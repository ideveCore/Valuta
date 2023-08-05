#!/usr/bin/env python
import logging
import json
import re
import requests


__author__ = "Hariom"

logger = logging.getLogger(__name__)

CODES = {
    "AFN": "Afghan Afghani",
    "ALL": "Albanian Lek",
    "DZD": "Algerian Dinar",
    "AOA": "Angolan Kwanza",
    "ARS": "Argentine Peso",
    "AMD": "Armenian Dram",
    "AWG": "Aruban Florin",
    "AUD": "Australian Dollar",
    "AZN": "Azerbaijani Manat",
    "BSD": "Bahamian Dollar",
    "BHD": "Bahraini Dinar",
    "BBD": "Bajan dollar",
    "BDT": "Bangladeshi Taka",
    "BYR": "Belarusian Ruble",
    "BYN": "Belarusian Ruble",
    "BZD": "Belize Dollar",
    "BMD": "Bermudan Dollar",
    "BTN": "Bhutan currency",
    "BTC": "Bitcoin",
    "BCH": "Bitcoin Cash",
    "BOB": "Bolivian Boliviano",
    "BAM": "Bosnia-Herzegovina Convertible Mark",
    "BWP": "Botswanan Pula",
    "BRL": "Brazilian Real",
    "BND": "Brunei Dollar",
    "BGN": "Bulgarian Lev",
    "BIF": "Burundian Franc",
    "XPF": "CFP Franc",
    "KHR": "Cambodian riel",
    "CAD": "Canadian Dollar",
    "CVE": "Cape Verdean Escudo",
    "KYD": "Cayman Islands Dollar",
    "XAF": "Central African CFA franc",
    "CLP": "Chilean Peso",
    "CLF": "Chilean Unit of Account (UF)",
    "CNY": "Chinese Yuan",
    "CNH": "Chinese Yuan (offshore)",
    "COP": "Colombian Peso",
    "KMF": "Comorian franc",
    "CDF": "Congolese Franc",
    "CRC": "Costa Rican Colón",
    "HRK": "Croatian Kuna",
    "CUP": "Cuban Peso",
    "CZK": "Czech Koruna",
    "DKK": "Danish Krone",
    "DJF": "Djiboutian Franc",
    "DOP": "Dominican Peso",
    "XCD": "East Caribbean Dollar",
    "EGP": "Egyptian Pound",
    "ETH": "Ether",
    "ETB": "Ethiopian Birr",
    "EUR": "Euro",
    "FJD": "Fijian Dollar",
    "GMD": "Gambian dalasi",
    "GEL": "Georgian Lari",
    "GHC": "Ghanaian Cedi",
    "GHS": "Ghanaian Cedi",
    "GIP": "Gibraltar Pound",
    "GTQ": "Guatemalan Quetzal",
    "GNF": "Guinean Franc",
    "GYD": "Guyanaese Dollar",
    "HTG": "Haitian Gourde",
    "HNL": "Honduran Lempira",
    "HKD": "Hong Kong Dollar",
    "HUF": "Hungarian Forint",
    "ISK": "Icelandic Króna",
    "INR": "Indian Rupee",
    "IDR": "Indonesian Rupiah",
    "IRR": "Iranian Rial",
    "IQD": "Iraqi Dinar",
    "ILS": "Israeli New Shekel",
    "JMD": "Jamaican Dollar",
    "JPY": "Japanese Yen",
    "JOD": "Jordanian Dinar",
    "KZT": "Kazakhstani Tenge",
    "KES": "Kenyan Shilling",
    "KWD": "Kuwaiti Dinar",
    "KGS": "Kyrgystani Som",
    "LAK": "Laotian Kip",
    "LBP": "Lebanese pound",
    "LSL": "Lesotho loti",
    "LRD": "Liberian Dollar",
    "LYD": "Libyan Dinar",
    "LTC": "Litecoin",
    "MOP": "Macanese Pataca",
    "MKD": "Macedonian Denar",
    "MGA": "Malagasy Ariary",
    "MWK": "Malawian Kwacha",
    "MYR": "Malaysian Ringgit",
    "MVR": "Maldivian Rufiyaa",
    "MRO": "Mauritanian Ouguiya (1973–2017)",
    "MUR": "Mauritian Rupee",
    "MXN": "Mexican Peso",
    "MDL": "Moldovan Leu",
    "MAD": "Moroccan Dirham",
    "MZM": "Mozambican metical",
    "MZN": "Mozambican metical",
    "MMK": "Myanmar Kyat",
    "TWD": "New Taiwan dollar",
    "NAD": "Namibian dollar",
    "NPR": "Nepalese Rupee",
    "ANG": "Netherlands Antillean Guilder",
    "NZD": "New Zealand Dollar",
    "NIO": "Nicaraguan Córdoba",
    "NGN": "Nigerian Naira",
    "NOK": "Norwegian Krone",
    "OMR": "Omani Rial",
    "PKR": "Pakistani Rupee",
    "PAB": "Panamanian Balboa",
    "PGK": "Papua New Guinean Kina",
    "PYG": "Paraguayan Guarani",
    "PHP": "Philippine Piso",
    "PLN": "Poland złoty",
    "GBP": "Pound sterling",
    "QAR": "Qatari Rial",
    "ROL": "Romanian Leu",
    "RON": "Romanian Leu",
    "RUR": "Russian Ruble",
    "RUB": "Russian Ruble",
    "RWF": "Rwandan franc",
    "SVC": "Salvadoran Colón",
    "SAR": "Saudi Riyal",
    "CSD": "Serbian Dinar",
    "RSD": "Serbian Dinar",
    "SCR": "Seychellois Rupee",
    "SLL": "Sierra Leonean Leone",
    "SGD": "Singapore Dollar",
    "PEN": "Sol",
    "SBD": "Solomon Islands Dollar",
    "SOS": "Somali Shilling",
    "ZAR": "South African Rand",
    "KRW": "South Korean won",
    "VEF": "Sovereign Bolivar",
    "XDR": "Special Drawing Rights",
    "LKR": "Sri Lankan Rupee",
    "SSP": "Sudanese pound",
    "SDG": "Sudanese pound",
    "SRD": "Surinamese Dollar",
    "SZL": "Swazi Lilangeni",
    "SEK": "Swedish Krona",
    "CHF": "Swiss Franc",
    "TJS": "Tajikistani Somoni",
    "TZS": "Tanzanian Shilling",
    "THB": "Thai Baht",
    "TOP": "Tongan Paʻanga",
    "TTD": "Trinidad & Tobago Dollar",
    "TND": "Tunisian Dinar",
    "TRY": "Turkish lira",
    "TMM": "Turkmenistan manat",
    "TMT": "Turkmenistan manat",
    "UGX": "Ugandan Shilling",
    "UAH": "Ukrainian hryvnia",
    "AED": "United Arab Emirates Dirham",
    "USD": "United States Dollar",
    "UYU": "Uruguayan Peso",
    "UZS": "Uzbekistani Som",
    "VND": "Vietnamese dong",
    "XOF": "West African CFA franc",
    "YER": "Yemeni Rial",
    "ZMW": "Zambian Kwacha"
}


def convert(currency_from, currency_to, amnt, replace_commas=True):
    """
    Used to convert amount from one currency to another
    :param currency_from: Currency code from which amount needs to be converted
    :param currency_to: Currency code in which amount needs to be converted to
    :param amnt: Amount which needs to be converted
    :param replace_commas: If True than the commas will be removed from converted amount and the converted amount will
        be like 70000 otherwise it will return with comma like 70,000
    :return: Json
    """
    # Validate the parameters
    if not isinstance(currency_from, str):
        raise TypeError("currency_from should be of type str, passed %s" % type(currency_from))

    if not isinstance(currency_to, str):
        raise TypeError("currency_to should be of type str, passed %s" % type(currency_to))

    if not isinstance(amnt, float) and not isinstance(amnt, int):
        raise TypeError("amount should be either int or float, passed %s" % type(amnt))

    url = "http://216.58.221.46/search?q=convert+{amount}+{frm}+to+{to}&hl=en&lr=lang_en".format(amount = str(amnt),
                                                                                                 frm    = currency_from,
                                                                                                 to     = currency_to)

    currency_from = currency_from.upper()
    currency_to   = currency_to.upper()

    # This will be returned as default if the given code are not present in our database
    default_response = {
        "from"     : currency_from,  # From currency code
        "to"       : currency_to,    # To currency code
        "amount"   : 0,              # Amount of currency to be returned
        "converted": False           # Flag indicating whether the currency is converted or not
    }

    try:
        currency_to_name   = CODES[currency_to]

        # Just to check whether this currency exists in out currency code base or not
        currency_from_name = CODES[currency_from]

        # If currency_to_name and currency_from_name is same then user is just trying to convert the same currency and
        # we need to return the same value

        if currency_to_name == currency_from_name:
            default_response["converted"] = True
            default_response["amount"]    = float(amnt)
            return json.dumps(default_response)

        # response = requests.get(url)
        response = requests.get(url, headers={"Range": "bytes=0-1"})

        html = response.text

        results = re.findall("[\d*\,]*\.\d* {currency_to_name}".format(currency_to_name=currency_to_name), html)

        # converted_amount_str = "0.0 {to}".format(to=currency_to)
        if results.__len__() > 0:
            converted_amount_str = results[0]
            converted_currency = re.findall('[\d*\,]*\.\d*', converted_amount_str)[0]

            if replace_commas:
                converted_currency = converted_currency.replace(',', '')

            default_response["amount"]    = converted_currency
            default_response["converted"] = True
            return json.dumps(default_response)
        else:
            raise Exception("Unable to convert currency, failed to fetch results from Google")

    except KeyError as error:
        logger.error("Invalid currency codes passed in parameters, original exception message is -> %s" % error)

    except TypeError as error:
        logger.error(error)

    except Exception as error:
        logger.error(error)

    finally:
        return json.dumps(default_response)
