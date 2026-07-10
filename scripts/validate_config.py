from pathlib import Path
import sys
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = PROJECT_ROOT / "config"

REQUIRED_ENVIRONMENTS = ["dev", "uat", "prod"]
VALID_LOG_LEVELS = ["debug", "information", "warning", "error"]


def load_yaml(file_path: Path) -> dict:
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except yaml.YAMLError as error:
        raise ValueError(f"Invalid YAML syntax: {error}")

    if not isinstance(data, dict):
        raise ValueError("Config file must contain a YAML object")

    return data


def validate_config(environment: str, config: dict) -> list[str]:
    errors = []

    if config.get("environment") != environment:
        errors.append(
            f"'environment' must be '{environment}', got '{config.get('environment')}'"
        )

    app = config.get("app")
    if not isinstance(app, dict):
        errors.append("'app' section is missing or invalid")
    else:
        if app.get("name") != "cloud-trade-api":
            errors.append("'app.name' must be 'cloud-trade-api'")

        if not app.get("version"):
            errors.append("'app.version' is required")

        if app.get("log_level") not in VALID_LOG_LEVELS:
            errors.append(
                f"'app.log_level' must be one of {VALID_LOG_LEVELS}"
            )

    trade_settings = config.get("trade_settings")
    if not isinstance(trade_settings, dict):
        errors.append("'trade_settings' section is missing or invalid")
    else:
        max_trade_count = trade_settings.get("max_trade_count")
        enable_mock_data = trade_settings.get("enable_mock_data")

        if not isinstance(max_trade_count, int) or max_trade_count <= 0:
            errors.append("'trade_settings.max_trade_count' must be a positive integer")

        if not isinstance(enable_mock_data, bool):
            errors.append("'trade_settings.enable_mock_data' must be true or false")

        if environment == "prod" and enable_mock_data is True:
            errors.append("Production config must not enable mock data")

    return errors


def main() -> int:
    all_errors = []

    for environment in REQUIRED_ENVIRONMENTS:
        file_path = CONFIG_DIR / f"{environment}.yml"

        if not file_path.exists():
            all_errors.append(f"{file_path} does not exist")
            continue

        try:
            config = load_yaml(file_path)
            errors = validate_config(environment, config)
        except ValueError as error:
            errors = [str(error)]

        if errors:
            all_errors.append(f"\n{file_path}:")
            all_errors.extend([f"  - {error}" for error in errors])
        else:
            print(f"✅ {file_path} is valid")

    if all_errors:
        print("\n❌ Config validation failed")
        for error in all_errors:
            print(error)
        return 1

    print("\n✅ All config files are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())