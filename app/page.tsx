"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { AlertCircle, BookOpen } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"

export default function BookPriceChecker() {
  const [bookName, setBookName] = useState("")
  const [model, setModel] = useState("openai")
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
      const response = await fetch(`http://localhost:500/api/get-price`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ bookName, model }),
      })

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`)
      }

      const data = await response.json()
      setPrice(data.price)
    } catch (err) {
      setError(`Failed to fetch price: ${err instanceof Error ? err.message : "Unknown error"}`)
    } finally {
      setLoading(false)
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
                <AlertDescription>{error}</AlertDescription>
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

