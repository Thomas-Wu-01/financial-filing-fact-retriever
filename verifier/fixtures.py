"""Authoritative fixed fixtures for the entirely synthetic closed corpus."""


def make_record(source_id, company, filing_type, period, period_basis, scope, metric, value, unit):
    return {
        "source_id": source_id,
        "company": company,
        "filing_type": filing_type,
        "period": period,
        "period_basis": period_basis,
        "scope": scope,
        "metric": metric,
        "value": value,
        "unit": unit,
    }


COMPANIES = ("Aster Vale Robotics", "Blue Harbor Foods", "Cinder Peak Energy")

RECORDS = (
    make_record("AV24-A-REV", COMPANIES[0], "Annual report", "FY2024", "full fiscal year", "Consolidated", "Revenue", "1250.40", "USD million"),
    make_record("AV24-A-OI", COMPANIES[0], "Annual report", "FY2024", "full fiscal year", "Consolidated", "Operating income", "-12.50", "USD million"),
    make_record("AV24-A-ASSET", COMPANIES[0], "Annual report", "FY2024", "fiscal year-end instant", "Consolidated", "Total assets", "980.00", "USD million"),
    make_record("AV25-A-REV", COMPANIES[0], "Annual report", "FY2025", "full fiscal year", "Consolidated", "Revenue", "1402.0", "USD million"),
    make_record("AV25-A-OI", COMPANIES[0], "Annual report", "FY2025", "full fiscal year", "Consolidated", "Operating income", "0.0", "USD million"),
    make_record("AV25-A-ASSET", COMPANIES[0], "Annual report", "FY2025", "fiscal year-end instant", "Consolidated", "Total assets", "1050.75", "USD million"),
    make_record("BH24-A-REV", COMPANIES[1], "Annual report", "FY2024", "full fiscal year", "Consolidated", "Revenue", "845000", "USD thousand"),
    make_record("BH24-A-OI", COMPANIES[1], "Annual report", "FY2024", "full fiscal year", "Consolidated", "Operating income", "52100.00", "USD thousand"),
    make_record("BH24-A-ASSET", COMPANIES[1], "Annual report", "FY2024", "fiscal year-end instant", "Consolidated", "Total assets", "612345.67", "USD thousand"),
    make_record("BH25-A-REV", COMPANIES[1], "Annual report", "FY2025", "full fiscal year", "Consolidated", "Revenue", "901250.5", "USD thousand"),
    make_record("BH25-A-OI", COMPANIES[1], "Annual report", "FY2025", "full fiscal year", "Consolidated", "Operating income", "60400", "USD thousand"),
    make_record("BH25-A-ASSET", COMPANIES[1], "Annual report", "FY2025", "fiscal year-end instant", "Consolidated", "Total assets", "650000.00", "USD thousand"),
    make_record("CP24-A-REV", COMPANIES[2], "Annual report", "FY2024", "full fiscal year", "Consolidated", "Revenue", "730.25", "EUR million"),
    make_record("CP24-A-OI", COMPANIES[2], "Annual report", "FY2024", "full fiscal year", "Consolidated", "Operating income", "88.6", "EUR million"),
    make_record("CP24-A-ASSET", COMPANIES[2], "Annual report", "FY2024", "fiscal year-end instant", "Consolidated", "Total assets", "1120.00", "EUR million"),
    make_record("CP25-A-REV", COMPANIES[2], "Annual report", "FY2025", "full fiscal year", "Consolidated", "Revenue", "680.00", "EUR million"),
    make_record("CP25-A-ASSET", COMPANIES[2], "Annual report", "FY2025", "fiscal year-end instant", "Consolidated", "Total assets", "1195.5", "EUR million"),
    make_record("AV24-Q4-REV", COMPANIES[0], "Quarterly report", "FY2024 Q4", "fiscal quarter", "Consolidated", "Revenue", "330.10", "USD million"),
    make_record("AV25-Q2-REV", COMPANIES[0], "Quarterly report", "FY2025 Q2", "fiscal quarter", "Consolidated", "Revenue", "351.25", "USD million"),
    make_record("BH24-Q4-REV", COMPANIES[1], "Quarterly report", "FY2024 Q4", "fiscal quarter", "Consolidated", "Revenue", "218750.00", "USD thousand"),
    make_record("BH25-Q2-REV", COMPANIES[1], "Quarterly report", "FY2025 Q2", "fiscal quarter", "Consolidated", "Revenue", "226500", "USD thousand"),
    make_record("CP24-Q4-REV", COMPANIES[2], "Quarterly report", "FY2024 Q4", "fiscal quarter", "Consolidated", "Revenue", "176.40", "EUR million"),
    make_record("CP25-Q2-REV", COMPANIES[2], "Quarterly report", "FY2025 Q2", "fiscal quarter", "Consolidated", "Revenue", "165.75", "EUR million"),
    make_record("AV24-S-AUTO", COMPANIES[0], "Annual report", "FY2024", "full fiscal year", "Segment: Automation", "Revenue", "455.60", "USD million"),
    make_record("AV25-S-AUTO", COMPANIES[0], "Annual report", "FY2025", "full fiscal year", "Segment: Automation", "Revenue", "510.00", "USD million"),
    make_record("BH24-S-FROZEN", COMPANIES[1], "Annual report", "FY2024", "full fiscal year", "Segment: Frozen Foods", "Revenue", "312000.0", "USD thousand"),
    make_record("BH25-S-FROZEN", COMPANIES[1], "Annual report", "FY2025", "full fiscal year", "Segment: Frozen Foods", "Revenue", "330500.25", "USD thousand"),
    make_record("CP24-S-SOLAR", COMPANIES[2], "Annual report", "FY2024", "full fiscal year", "Segment: Solar", "Revenue", "280.00", "EUR million"),
    make_record("CP25-S-SOLAR", COMPANIES[2], "Annual report", "FY2025", "full fiscal year", "Segment: Solar", "Revenue", "245.5", "EUR million"),
)


def record_by_source(source_id):
    for record in RECORDS:
        if record["source_id"] == source_id:
            return record
    return None


def matching_record(company, period, scope, metric):
    for record in RECORDS:
        if (
            record["company"] == company
            and record["period"] == period
            and record["scope"] == scope
            and record["metric"] == metric
        ):
            return record
    return None


def excerpt(record):
    return (
        "SYNTHETIC FILING EXCERPT — not a real SEC filing.\n"
        f"Source ID: {record['source_id']}\n"
        f"Company: {record['company']}\n"
        f"Filing: {record['filing_type']}\n"
        f"Period: {record['period']} ({record['period_basis']})\n"
        f"Scope: {record['scope']}\n"
        f"Metric: {record['metric']}\n"
        f"Reported fact: {record['metric']} was {record['value']} {record['unit']}.\n"
        f"Citation: {record['source_id']}"
    )
