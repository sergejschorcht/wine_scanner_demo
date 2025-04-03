"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { AlertCircle, BookOpen, ServerIcon } from "lucide-react"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

export default function BookPriceChecker() {
  const [bookName, setBookName] = useState("")
  const [model, setModel] = useState("openai")
  const [formatType, setFormatType] = useState("hardcover")
  const [price, setPrice] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!bookName.trim()) {
      setError("Please enter a book name")
      return
    }

    setLoading(true)
    setError(null)
    setPrice(null)

    try {
      // Add a timeout to prevent long waits if the server is down
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000);
      
      const response = await fetch(`http://localhost:5000/api/retrieve`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
          book_name: bookName, 
          format_type: formatType, 
          model 
        }),
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server error (${response.status}): ${errorText}`);
      }

      const data = await response.json();
      setPrice(data.price);
    } catch (err) {
      if (err.name === 'AbortError') {
        setError("Request timed out. Please check if the API server is running at http://localhost:5000");
      } else if (err instanceof TypeError && err.message.includes('fetch')) {
        setError("Failed to connect to the API server. Please make sure it's running at http://localhost:5000");
      } else {
        setError(`${err instanceof Error ? err.message : "Unknown error"}. Check the console for more details.`);
      }
      console.error("API Request Error:", err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-2xl flex items-center gap-2">
            <BookOpen className="h-5 w-5" />
            Book Price Checker
          </CardTitle>
          <CardDescription>Enter a book name to get its price from different AI models</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="book-name">Book Name</Label>
              <Input
                id="book-name"
                placeholder="Enter book name"
                value={bookName}
                onChange={(e) => setBookName(e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="format-type">Format Type</Label>
              <Select value={formatType} onValueChange={setFormatType}>
                <SelectTrigger id="format-type">
                  <SelectValue placeholder="Select format" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="hardcover">Hardcover</SelectItem>
                  <SelectItem value="paperback">Paperback</SelectItem>
                  <SelectItem value="ebook">E-Book</SelectItem>
                  <SelectItem value="audiobook">Audiobook</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="model">AI Model</Label>
              <Select value={model} onValueChange={setModel}>
                <SelectTrigger id="model">
                  <SelectValue placeholder="Select model" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="openai">OpenAI</SelectItem>
                  <SelectItem value="gemini">Gemini</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Checking Price..." : "Get Price"}
            </Button>

            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>
                  {error}
                  {error.includes('API server') && (
                    <p className="mt-2 text-xs">
                      Make sure your backend server is running with the command:<br/>
                      <code className="bg-gray-800 text-white px-1 py-0.5 rounded text-xs">
                        python app.py
                      </code> or similar in your API directory.
                    </p>
                  )}
                </AlertDescription>
              </Alert>
            )}

            {price !== null && (
              <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-md">
                <p className="text-sm text-gray-500">Price:</p>
                <p className="text-2xl font-bold">${price} USD</p>
              </div>
            )}
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

