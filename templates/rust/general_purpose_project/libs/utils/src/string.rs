pub fn capitalise(s: impl AsRef<str>) -> String {
    let mut c = s.as_ref().chars();

    match c.next() {
        None => String::new(),
        Some(f) => f.to_uppercase().collect::<String>() + c.as_str(),
    }
}


pub fn trim_first_last_chars(s: impl AsRef<str>) -> String {
    let mut chars = s.as_ref().chars();
    chars.next();
    chars.next_back();

    return String::from(chars.as_str())
}


pub fn trim_last_char(s: impl AsRef<str>) -> String {
    let mut chars = s.as_ref().chars();
    chars.next_back();

    return String::from(chars.as_str())
}
