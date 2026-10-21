//! Rust-voorbeeld van de Flask-cookie-app, uitgevoerd met Axum.
//!
//! Voeg deze dependencies toe aan `Cargo.toml`:
//! ```toml
//! axum = "0.8"
//! tokio = { version = "1", features = ["macros", "rt-multi-thread", "net"] }
//! ```

use axum::{
    body::Body,
    http::{
        header::{COOKIE, CONTENT_TYPE, SET_COOKIE},
        HeaderMap, HeaderValue,
    },
    response::Response,
    routing::get,
    Router,
};
use tokio::net::TcpListener;

const COOKIE_MAX_AGE_SECONDS: u64 = 60 * 60 * 24 * 30;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let app = Router::new().route("/", get(index));
    let listener = TcpListener::bind("127.0.0.1:3000").await?;

    println!("Server actief op http://127.0.0.1:3000");
    axum::serve(listener, app).await?;

    Ok(())
}

/// Toon de bezoeksteller en sla de bijgewerkte waarde op in een cookie.
async fn index(headers: HeaderMap) -> Response {
    let counter = read_counter(&headers).saturating_add(1);
    let cookie = format!(
        "teller={counter}; Max-Age={COOKIE_MAX_AGE_SECONDS}; Path=/; HttpOnly; SameSite=Lax"
    );
    let body = format!(
        "<!doctype html>\
         <html lang=\"nl\">\
         <head><meta charset=\"utf-8\"><title>Bezoeksteller</title></head>\
         <body>De waarde van het cookie is: {counter}</body>\
         </html>"
    );

    let mut response = Response::new(Body::from(body));
    response.headers_mut().insert(
        CONTENT_TYPE,
        HeaderValue::from_static("text/html; charset=utf-8"),
    );
    response.headers_mut().insert(
        SET_COOKIE,
        cookie
            .parse()
            .expect("De cookieheader bevat alleen vaste tekst en cijfers"),
    );
    response
}

/// Lees de teller uit de cookieheader; ongeldige of ontbrekende waarden zijn nul.
fn read_counter(headers: &HeaderMap) -> u64 {
    headers
        .get(COOKIE)
        .and_then(|value| value.to_str().ok())
        .and_then(|cookies| {
            cookies.split(';').find_map(|cookie| {
                let (name, value) = cookie.trim().split_once('=')?;
                if name == "teller" {
                    Some(value.parse::<u64>().unwrap_or(0))
                } else {
                    None
                }
            })
        })
        .unwrap_or(0)
}
