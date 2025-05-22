use nom::{
    IResult, bytes::complete::tag, bytes::complete::take_until, character::complete::alpha1,
};
use pyo3::prelude::{Bound, PyModule, PyResult, pyclass, pyfunction, pymodule, wrap_pyfunction};
use pyo3::types::PyModuleMethods;

// --- LogEntry Struct ---
#[pyclass]
#[derive(Debug, PartialEq, Eq, Clone)]
pub struct LogEntry {
    #[pyo3(get)]
    pub timestamp: String,
    #[pyo3(get)]
    pub level: String,
    #[pyo3(get)]
    pub message: String,
}

// --- Rust Parsing Function ---
fn _parse_log_line(input: &str) -> IResult<&str, LogEntry> {
    let log_levels = ["INFO", "WARN", "ERROR", "DEBUG"];

    let space = tag(" ");
    let (input, _) = tag("[")(input)?;
    let (input, date) = take_until(" ")(input)?;
    let (input, _) = space(input)?;
    let (input, time) = take_until("]")(input)?;
    let (input, _) = tag("]")(input)?;
    let (input, _) = space(input)?;
    let (input, level) = alpha1(input)?;

    match log_levels.contains(&level) {
        true => (),
        false => {
            return Err(nom::Err::Error(nom::error::Error::new(
                input,
                nom::error::ErrorKind::IsNot,
            )));
        }
    }

    let (input, _) = tag(": ")(input)?;
    let (input, message) =
        take_until("\n")(input).or_else(|_: nom::Err<nom::error::Error<&str>>| Ok(("", input)))?;

    return Ok((
        input,
        LogEntry {
            timestamp: date.to_string() + " " + &time.to_string(),
            level: level.to_string(),
            message: message.to_string(),
        },
    ));
}

#[pyfunction]
fn parse_log_line(input: &str) -> Option<LogEntry> {
    let (remaining, entry) = _parse_log_line(input).ok()?;
    if remaining.is_empty() {
        Some(entry)
    } else {
        None
    }
}
// --- PyO3 Module Definition ---
#[pymodule(name = "rslib")]
fn rslib(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse_log_line, m)?)?;
    m.add_class::<LogEntry>()?;
    Ok(())
}

// --- Rust Tests ---
#[cfg(test)]
mod tests {
    use super::*; // Import items from the parent module
    use pretty_assertions::assert_eq;

    #[test]
    fn test_parse_valid_info_log() {
        let line = "[2023-10-27 14:30:05] INFO: User logged in.";
        let expected = LogEntry {
            timestamp: "2023-10-27 14:30:05".to_string(),
            level: "INFO".to_string(),
            message: "User logged in.".to_string(),
        };
        let (remaining, parsed) = _parse_log_line(line).expect("Should parse successfully");
        assert_eq!(remaining, ""); // Ensure the entire line was consumed
        assert_eq!(parsed, expected);
    }

    #[test]
    fn test_parse_valid_warn_log() {
        let line = "[2024-01-15 08:00:10] WARN: Disk space low.";
        let expected = LogEntry {
            timestamp: "2024-01-15 08:00:10".to_string(),
            level: "WARN".to_string(),
            message: "Disk space low.".to_string(),
        };
        let (remaining, parsed) = _parse_log_line(line).expect("Should parse successfully");
        assert_eq!(remaining, "");
        assert_eq!(parsed, expected);
    }

    #[test]
    fn test_parse_valid_error_log_no_newline() {
        // Test a line that doesn't end with a newline
        let line = "[2025-05-22 09:14:52] ERROR: Database connection failed. Retrying...";
        let expected = LogEntry {
            timestamp: "2025-05-22 09:14:52".to_string(),
            level: "ERROR".to_string(),
            message: "Database connection failed. Retrying...".to_string(),
        };
        let (remaining, parsed) = _parse_log_line(line).expect("Should parse successfully");
        assert_eq!(remaining, "");
        assert_eq!(parsed, expected);
    }

    #[test]
    fn test_parse_invalid_format() {
        // These should result in an Err from nom
        assert!(_parse_log_line("Invalid log line").is_err());
        assert!(_parse_log_line("[2023-10-27] INFO: Missing time").is_err());
        assert!(_parse_log_line("2023-10-27 14:30:05 INFO: No brackets").is_err());
        assert!(_parse_log_line("[2023-10-27 14:30:05] HELLO: Unknown level").is_err()); // 'HELLO' not in regex
    }

    #[test]
    fn test_parse_empty_line() {
        assert!(_parse_log_line("").is_err());
        assert!(_parse_log_line("   ").is_err());
    }

    // --- Test PyO3 interface ---
    #[test]
    fn test_py_parse_valid_log() {
        let line = "[2023-10-27 14:30:05] INFO: User logged in.";
        let (_, entry) = _parse_log_line(line).unwrap(); // Unwrap the PyResult
        assert_eq!(entry.timestamp, "2023-10-27 14:30:05");
        assert_eq!(entry.level, "INFO");
        assert_eq!(entry.message, "User logged in.");
    }

    #[test]
    fn test_py_parse_invalid_log() {
        let line = "This is not a log line.";
        let result = _parse_log_line(line);
        assert!(result.is_err());
    }
}
