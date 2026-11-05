use std::io::{self, BufRead, Write};

fn count_primes(n: u64) -> u64 {
    if n < 2 {
        return 0;
    }
    let n = n as usize;
    let mut sieve = vec![true; n + 1];
    sieve[0] = false;
    sieve[1] = false;
    let mut i = 2;
    while i * i <= n {
        if sieve[i] {
            let mut j = i * i;
            while j <= n {
                sieve[j] = false;
                j += i;
            }
        }
        i += 1;
    }
    sieve.iter().filter(|&&p| p).count() as u64
}

fn handle_line(line: &str) -> Option<String> {
    let line = line.trim();
    if line.is_empty() {
        return None;
    }
    let mut parts = line.split_whitespace();
    match (parts.next(), parts.next(), parts.next()) {
        (Some("RUN"), Some(arg), None) => match arg.parse::<u64>() {
            Ok(n) => Some(format!("RESULT {}", count_primes(n))),
            Err(_) => Some("ERROR invalid_number".to_string()),
        },
        _ => Some("ERROR unknown_command".to_string()),
    }
}

fn main() {
    let stdin = io::stdin();
    let stdout = io::stdout();
    let mut out = stdout.lock();

    writeln!(out, "READY").unwrap();
    out.flush().unwrap();

    for line in stdin.lock().lines() {
        let line = match line {
            Ok(l) => l,
            Err(e) => {
                eprintln!("read error: {}", e);
                break;
            }
        };
        if line.trim() == "QUIT" {
            break;
        }
        if let Some(reply) = handle_line(&line) {
            writeln!(out, "{}", reply).unwrap();
            out.flush().unwrap();
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn small_values() {
        assert_eq!(count_primes(0), 0);
        assert_eq!(count_primes(1), 0);
        assert_eq!(count_primes(2), 1);
        assert_eq!(count_primes(10), 4);
    }

    #[test]
    fn protocol_vectors() {
        assert_eq!(count_primes(1000), 168);
        assert_eq!(count_primes(10000), 1229);
    }

    #[test]
    fn run_command() {
        assert_eq!(handle_line("RUN 10000").as_deref(), Some("RESULT 1229"));
        assert_eq!(handle_line("RUN 1000").as_deref(), Some("RESULT 168"));
    }

    #[test]
    fn bad_input() {
        assert_eq!(handle_line("RUN abc").as_deref(), Some("ERROR invalid_number"));
        assert_eq!(handle_line("HELLO").as_deref(), Some("ERROR unknown_command"));
        assert_eq!(handle_line("   "), None);
    }
}
