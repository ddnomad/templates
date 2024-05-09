#[allow(clippy::module_inception)]
mod cmdline;
mod hello_world;

pub(crate) use cmdline::{Subcommand, parse};
pub(crate) use hello_world::{HelloWorldCommand, HelloWorldSubcommand};
