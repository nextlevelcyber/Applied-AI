import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const workbook = Workbook.create();

const report = workbook.worksheets.add("Report");
const tests = workbook.worksheets.add("Black-Box Tests");
const refs = workbook.worksheets.add("References");

function styleTitle(range) {
  range.format.fill.color = "#1F4E78";
  range.format.font.color = "#FFFFFF";
  range.format.font.bold = true;
  range.format.font.size = 16;
}

function styleSection(range) {
  range.format.fill.color = "#D9EAF7";
  range.format.font.bold = true;
}

function styleBody(range) {
  range.format.wrapText = true;
  range.format.verticalAlignment = "Top";
}

function styleTableHeader(range) {
  range.format.fill.color = "#1F4E78";
  range.format.font.color = "#FFFFFF";
  range.format.font.bold = true;
  range.format.wrapText = true;
}

report.showGridLines = false;
report.getRange("A1:D1").merge();
report.getRange("A1").values = [["Historical Weather Data ICA Report"]];
styleTitle(report.getRange("A1"));

const sections = [
  ["1. Introduction", "This project implements a Python application for processing historical weather data from the supplied SQLite database and the Open-Meteo archive API. The work is organised into three phases: database querying, chart generation, and API retrieval/storage. Shared validation and connection logic is placed in ICA/common.py, while ICA/main.py provides a single demo/menu/CLI entry point. This structure keeps the phase files easy to inspect while avoiding repeated connection and validation code."],
  ["2. Software Tools", "SQLite is appropriate because the dataset is relational, local, and modest in size. It supports joins, grouping, date filtering, and aggregates, which are central to the temperature and precipitation queries. Its limitation is scalability: a production weather platform with concurrent users would need a server database and stronger migration controls.\n\nMatplotlib is used for Phase 2 because it can generate reproducible PNG evidence without requiring a web dashboard. The charts include daily precipitation, city comparisons, country averages, grouped weather metrics, a min/max line chart, and a temperature/rainfall scatter plot. Matplotlib gives good control over labels and exported files, although it requires more manual layout work than higher-level visualisation packages.\n\nRequests is used for Phase 3 because it allows direct HTTP request handling. The application builds Open-Meteo parameters itself, sets timezone, applies a timeout, and validates the JSON response before storage. This is suitable for the ICA requirement to write custom API request code. The main limitation is that live API calls can fail due to network problems, service changes, or malformed responses.\n\nVisual Studio Code is useful for Python editing, terminal runs, source control, and database inspection extensions. However, an editor does not prove correctness, so the project also includes automated tests and chart evidence."],
  ["3. Security And Risk", "The main risks are invalid input, SQL injection, dependency risk, duplicate data, and external API failure. SQL values are passed through placeholders rather than string concatenation. Dates and years are validated, including reversed date ranges, before database queries or API calls are made. City lists used in chart queries are converted to integers before SQL placeholder generation.\n\nThird-party packages introduce maintenance risk. requirements.txt declares matplotlib and requests, but a production system should also pin versions, monitor vulnerabilities, and use controlled deployment. The solution uses only sqlite3 for Phase 1 database work, sqlite3 plus matplotlib for Phase 2 visualisation, and requests for Phase 3 API access. Other standard-library modules are limited to validation, paths, typing, temporary test databases, and CLI support.\n\nOpen-Meteo dependency is another risk. The parser checks required fields and matching array lengths before inserting data. Network errors are wrapped in WeatherApiError, and automated tests mock API calls so the test suite remains reliable. Database updates delete the same city/date row before inserting refreshed data, reducing duplicate record risk. A production schema would further improve this with a unique constraint on (city_id, date)."],
  ["4. Programming Concepts And Data Structures", "The solution uses small functions with clear responsibilities: query functions return rows, chart functions save PNG files, API functions build parameters and parse JSON, and storage functions update SQLite. Lists hold query results and parsed weather rows. Dictionaries represent parsed API records using named fields such as date, mean_temp, and precipitation. A City dataclass stores the id, name, latitude, longitude, and timezone required by Open-Meteo, which is clearer than passing separate values through several functions.\n\nException handling is used for missing database files, invalid dates, unknown cities, malformed API payloads, and network failures. Automated tests use unittest, temporary database copies, and mocked HTTP requests. This protects the supplied database while checking behaviour from the outside: expected rows, generated files, rejected invalid input, and stable error handling."],
  ["5. Conclusion", "The application meets the ICA requirements by implementing SQLite queries, Matplotlib visualisations, Open-Meteo retrieval, database storage, a reusable code structure, a CLI/menu entry point, and repeatable tests. The design is intentionally small, but it demonstrates relational querying, validation, structured data, external API use, chart evidence, and black-box style testing."],
];

let row = 3;
for (const [heading, body] of sections) {
  report.getRange(`A${row}:D${row}`).merge();
  report.getRange(`A${row}`).values = [[heading]];
  styleSection(report.getRange(`A${row}`));
  row += 1;
  report.getRange(`A${row}:D${row + 1}`).merge();
  report.getRange(`A${row}`).values = [[body]];
  styleBody(report.getRange(`A${row}`));
  row += 3;
}
report.getRange("A:D").format.columnWidth = 24;
report.getRange("A1:D22").format.borders = { preset: "outside", style: "thin", color: "#BFBFBF" };

tests.showGridLines = false;
tests.getRange("A1:G1").merge();
tests.getRange("A1").values = [["Appendix A: Black-Box Test Plan"]];
styleTitle(tests.getRange("A1"));
const testRows = [
  ["Test ID", "Phase", "Feature/function", "Input", "Expected result", "Actual result", "Pass/Fail"],
  ["BB-001", "Phase 1", "List countries", "select_all_countries", "Two countries shown", "2 rows returned", "PASS"],
  ["BB-002", "Phase 1", "List cities", "select_all_cities", "Four cities shown", "4 rows returned", "PASS"],
  ["BB-003", "Phase 1", "Annual temperature", "City 1, 2024", "One average temperature", "One float result", "PASS"],
  ["BB-004", "Phase 1", "Seven-day precipitation", "City 1, 2024-01-01", "7 days counted", "days_found = 7", "PASS"],
  ["BB-005", "Phase 1", "Invalid date", "2024-99-99", "Validation error", "ValueError raised", "PASS"],
  ["BB-006", "All phases", "Reversed date range", "2024-02-01 to 2024-01-01", "Validation error", "ValueError raised", "PASS"],
  ["BB-007", "Phase 2", "Chart creation", "7-day precipitation chart", "PNG created", "Non-empty PNG created", "PASS"],
  ["BB-008", "Phase 2", "Empty city list", "[]", "Validation error", "ValueError raised", "PASS"],
  ["BB-009", "Phase 2", "Full chart evidence", "python3 -m ICA.main charts", "Six charts generated", "Six PNG files created", "PASS"],
  ["BB-010", "Phase 3", "Parse API JSON", "Mock two-day payload", "Two weather rows", "2 rows parsed", "PASS"],
  ["BB-011", "Phase 3", "Replace existing row", "Same city/date", "One updated row remains", "Count 1, value updated", "PASS"],
  ["BB-012", "Phase 3", "Network error", "Mock timeout", "Controlled API error", "WeatherApiError raised", "PASS"],
  ["BB-013", "CLI", "Demo command", "python3 -m ICA.main demo", "Queries print and charts save", "Demo completed", "PASS"],
];
tests.getRange(`A3:G${testRows.length + 2}`).values = testRows;
styleTableHeader(tests.getRange("A3:G3"));
styleBody(tests.getRange(`A4:G${testRows.length + 2}`));
tests.getRange(`A3:G${testRows.length + 2}`).format.borders = { preset: "all", style: "thin", color: "#D9D9D9" };
tests.getRange("A:G").format.columnWidth = 20;
tests.freezePanes.freezeRows(3);

refs.showGridLines = false;
refs.getRange("A1:B1").merge();
refs.getRange("A1").values = [["References"]];
styleTitle(refs.getRange("A1"));
const references = [
  ["Hunter, J.D. (2007)", "Matplotlib: A 2D graphics environment, Computing in Science and Engineering, 9(3), pp. 90-95."],
  ["Open-Meteo (2024)", "Historical Weather API documentation. https://open-meteo.com/en/docs/historical-weather-api"],
  ["Python Software Foundation (2024)", "sqlite3: DB-API 2.0 interface for SQLite databases. https://docs.python.org/3/library/sqlite3.html"],
  ["Requests (2024)", "Requests: HTTP for Humans documentation. https://requests.readthedocs.io/"],
  ["SQLite Consortium (2024)", "About SQLite. https://www.sqlite.org/about.html"],
];
refs.getRange(`A3:B${references.length + 2}`).values = [["Reference", "Details"], ...references];
styleTableHeader(refs.getRange("A3:B3"));
styleBody(refs.getRange(`A4:B${references.length + 3}`));
refs.getRange(`A3:B${references.length + 3}`).format.borders = { preset: "all", style: "thin", color: "#D9D9D9" };
refs.getRange("A:A").format.columnWidth = 28;
refs.getRange("B:B").format.columnWidth = 80;

const errorScan = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 50 },
  summary: "formula error scan",
});
console.log(errorScan.ndjson);

await workbook.render({ sheetName: "Report", autoCrop: "all", scale: 1, format: "png" });
await workbook.render({ sheetName: "Black-Box Tests", autoCrop: "all", scale: 1, format: "png" });
await workbook.render({ sheetName: "References", autoCrop: "all", scale: 1, format: "png" });

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save("REPORT_AND_TESTING.xlsx");
