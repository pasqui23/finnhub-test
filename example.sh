#!/bin/sh
source .env
export FINNHUB_API_TOKEN
cli="poetry run python ./cli.py"

$cli save-forex OANDA:EUR_USD
$cli print-forex OANDA:EUR_USD

$cli save-stock AAPL
$cli print-company-profile AAPL
$cli print-stock AAPL