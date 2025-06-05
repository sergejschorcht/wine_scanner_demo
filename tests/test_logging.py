from api.core.client.logging import Logger


def test_logger_import(tmp_path):
    log_file = tmp_path / "log.txt"
    Logger(debug_mode=True, file=str(log_file))
