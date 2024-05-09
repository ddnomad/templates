#[derive(clap::Parser)]
#[command(
	author = clap::crate_authors!("\n"),
	about = "General purpose Rust project template",
	version,
	color = clap::ColorChoice::Auto
)]
pub(crate) struct Cmdline {
    #[arg(help = "Logging filter (overrides RUST_LOG)", long, short = 'l')]
    pub(crate) log_filter: Option<String>,

    #[command(subcommand)]
    pub(crate) subcommand: Subcommand,
}


#[derive(clap::Subcommand)]
pub(crate) enum Subcommand {
    HelloWorld(super::HelloWorldCommand),
}


pub(super) fn die(error_kind: clap::error::ErrorKind, message: impl AsRef<str>) {
    use clap::CommandFactory;

    Cmdline::command()
        .error(error_kind, message.as_ref())
        .exit();
}


pub(crate) fn parse() -> Cmdline {
    use clap::Parser;

    Cmdline::parse()
}
