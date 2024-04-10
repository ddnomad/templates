pub struct SuspendProgressWriter<W: std::io::Write> {
    writer: W,
    progress: Option<indicatif::MultiProgress>,
}


impl<W: std::io::Write> SuspendProgressWriter<W> {
    fn new<F: Fn() -> W>(make_writer: F, progress: Option<indicatif::MultiProgress>) -> Self {
        let writer = make_writer();
        Self { writer, progress }
    }
}


impl<W: std::io::Write> std::io::Write for SuspendProgressWriter<W> {
    fn write(&mut self, buf: &[u8]) -> std::io::Result<usize> {
        match self.progress {
            Some(ref p) => p.suspend(|| self.writer.write(buf)),
            None => self.writer.write(buf),
        }
    }
    
    fn flush(&mut self) -> std::io::Result<()> {
        self.writer.flush()
    }
}


pub fn tracing_subscriber<S: AsRef<str>>(
    log_filter: Option<S>,
    progress: Option<indicatif::MultiProgress>,
) -> Result<
    tracing_subscriber::fmt::SubscriberBuilder<
        tracing_subscriber::fmt::format::DefaultFields,
        tracing_subscriber::fmt::format::Format,
        tracing_subscriber::EnvFilter,
        impl Fn() -> SuspendProgressWriter<std::io::Stderr>,
    >,
    tracing_subscriber::filter::ParseError,
> {
    let subscriber = tracing_subscriber::fmt()
        .with_thread_names(true)
        .with_writer(move || SuspendProgressWriter::new(std::io::stderr, progress.clone()));
    
    let subscriber = match log_filter {
        Some(f) => subscriber.with_env_filter(tracing_subscriber::EnvFilter::try_new(f)?),
        None => subscriber.with_env_filter(tracing_subscriber::EnvFilter::from_default_env()),
    };
    
    Ok(subscriber)
}
