// Purpose: Print "Hello, world!"
// Test: `$ rustc --out-dir build/ main.rs && ./build/main`
// Input: None
// Output: "Hello, world!"
// Reference: https://doc.rust-lang.org/book/ch01-02-hello-world.html


// 1. The "main" function is  special: it is always the first  code that runs in
// every executable Rust program.
// v--v
fn main() {
// 2. In Rust, by convention, we indent with four spaces, not with a tab.
//vv
    println!("Hello, world!");
    //     ^
    // 3. The bang indicates that we're calling a macro; not a function.
    // https://doc.rust-lang.org/reference/macros.html#macro-invocation
    // https://doc.rust-lang.org/std/macro.println.html

    println!("Hello, world!");
    //                       ^
    // 4. The semicolon indicates that this expression is over and the next one
    // is ready to begin.  Most lines of Rust code end with a semicolon.
}
