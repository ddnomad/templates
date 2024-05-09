#[derive(clap::Parser)]
#[command(about = "Hello world command")]
pub(crate) struct HelloWorldCommand {
	#[clap(subcommand)]
	pub(crate) subcommand: HelloWorldSubcommand
}


#[derive(clap::Subcommand)]
pub(crate) enum HelloWorldSubcommand {
	#[command(about = "Greet")]
	Greet {}
}
