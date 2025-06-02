use pyo3::prelude::{
    Bound, PyModule, PyResult, pyclass, pyfunction, pymethods, pymodule, wrap_pyfunction,
};
use pyo3::types::PyModuleMethods;
use rand::Rng;
use std::fs::File;
use std::io::{BufRead, BufReader};

use regex::Regex;

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

#[pyclass]
pub struct Parser {
    pattern: Regex,
}

#[pymethods]
impl Parser {
    #[new]
    pub fn new() -> Self {
        Self {
            pattern: Regex::new(
                r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (INFO|WARN|ERROR|DEBUG): (.*)",
            )
            .unwrap(),
        }
    }

    pub fn parse_log_line(&self, line: &str) -> Option<LogEntry> {
        self.pattern.captures(line).map(|caps| LogEntry {
            timestamp: caps[1].to_string(),
            level: caps[2].to_string(),
            message: caps[3].to_string(),
        })
    }

    pub fn parse_log_file(&self, file_path: &str) -> Vec<LogEntry> {
        let file = File::open(file_path).unwrap();
        let reader = BufReader::new(file);
        reader
            .lines()
            .map(|line| self.parse_log_line(&line.unwrap()))
            .filter(|line| line.is_some())
            .map(|line| line.unwrap())
            .collect()
    }

    pub fn parse_log_lines_no_return(&self, file_path: &str) {
        let file = File::open(file_path).unwrap();
        let reader = BufReader::new(file);
        let lines = reader
            .lines()
            .map(|line| self.parse_log_line(&line.unwrap()))
            .filter(|line| line.is_some())
            .map(|line| line.unwrap())
            .collect::<Vec<LogEntry>>();
        lines.iter().count();
    }

    pub fn estimate_pi(&self, num_samples: i32) -> f64 {
        let mut rng = rand::rng();
        let mut inside_circle = 0;

        for _ in 0..num_samples {
            let x: f64 = rng.random();
            let y: f64 = rng.random();
            let distance_squared = x.powi(2) + y.powi(2);
            if distance_squared <= 1.0 {
                inside_circle += 1;
            }
        }
        (inside_circle as f64 / num_samples as f64) * 4.0
    }
}

// --- PyO3 Module Definition ---
#[pymodule(name = "rslib")]
fn rslib(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // m.add_function(wrap_pyfunction!(parse_log_line_py, m)?)?;
    // m.add_function(wrap_pyfunction!(parse_log_file, m)?)?;
    m.add_class::<Parser>()?;
    m.add_class::<LogEntry>()?;
    Ok(())
}

// --- Rust Tests ---
#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_parse_valid_info_log() {
        let line = "[2023-10-27 14:30:05] INFO: User logged in.";
        let expected = LogEntry {
            timestamp: "2023-10-27 14:30:05".to_string(),
            level: "INFO".to_string(),
            message: "User logged in.".to_string(),
        };
        let parser = Parser::new();
        let parsed = parser
            .parse_log_line(line)
            .expect("Should parse successfully");
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
        let parser = Parser::new();
        let parsed = parser
            .parse_log_line(line)
            .expect("Should parse successfully");
        assert_eq!(parsed, expected);
    }

    #[test]
    fn test_parse_valid_error_log_no_newline() {
        let line = "[2025-05-22 09:14:52] ERROR: Database connection failed. Retrying...";
        let expected = LogEntry {
            timestamp: "2025-05-22 09:14:52".to_string(),
            level: "ERROR".to_string(),
            message: "Database connection failed. Retrying...".to_string(),
        };
        let parser = Parser::new();
        let parsed = parser
            .parse_log_line(line)
            .expect("Should parse successfully");
        assert_eq!(parsed, expected);
    }

    #[test]
    fn test_parse_invalid_format() {
        let parser = Parser::new();
        assert!(parser.parse_log_line("Invalid log line").is_none());
        assert!(
            parser
                .parse_log_line("[2023-10-27] INFO: Missing time")
                .is_none()
        );
        assert!(
            parser
                .parse_log_line("2023-10-27 14:30:05 INFO: No brackets")
                .is_none()
        );
        assert!(
            parser
                .parse_log_line("[2023-10-27 14:30:05] HELLO: Unknown level")
                .is_none()
        );
    }

    #[test]
    fn test_parse_empty_line() {
        let parser = Parser::new();
        assert!(parser.parse_log_line("").is_none());
        assert!(parser.parse_log_line("   ").is_none());
    }

    #[test]
    fn test_py_parse_valid_log() {
        let line = "[2023-10-27 14:30:05] INFO: User logged in.";
        let parser = Parser::new();
        let entry = parser.parse_log_line(line).unwrap();
        assert_eq!(entry.timestamp, "2023-10-27 14:30:05");
        assert_eq!(entry.level, "INFO");
        assert_eq!(entry.message, "User logged in.");
    }

    #[test]
    fn test_py_parse_invalid_log() {
        let line = "This is not a log line.";
        let parser = Parser::new();
        let result = parser.parse_log_line(line);
        assert!(result.is_none());
    }
}
