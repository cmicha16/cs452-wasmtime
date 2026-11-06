# Stage 1: Build the Rust application
FROM rust:1.99.1-bookworm AS builder

WORKDIR /app

# Copy Rust project files
COPY benchmark/Cargo.toml benchmark/Cargo.lock ./
COPY benchmark/src ./src

# Run tests and compile in release mode
RUN cargo test --locked
RUN cargo build --release --locked

# Stage 2: Minimal runtime environment
FROM debian:bookworm-slim

WORKDIR /app

# Copy the compiled executable
COPY --from=builder /app/target/release/benchmark /app/benchmark

# Start the benchmark application
ENTRYPOINT ["/app/benchmark"]