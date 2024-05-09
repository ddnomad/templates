pub fn progress_bar(label: String, length: usize) -> indicatif::ProgressBar {
    let progress_bar = indicatif::ProgressBar::new(length as u64)
        .with_style(progress_style())
        .with_prefix(label);

    progress_bar.enable_steady_tick(std::time::Duration::from_millis(100));
    progress_bar
}


pub fn progress_style() -> indicatif::ProgressStyle {
    let template = "[{elapsed_precise}] {prefix} {wide_bar:.cyan/blue} {human_pos}/{human_len} ({percent}%, {per_sec})";

    indicatif::ProgressStyle::with_template(template)
        .expect("failed to create progress bar style from a template")
        .progress_chars("█░")
}
