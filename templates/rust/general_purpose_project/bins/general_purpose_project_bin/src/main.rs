#[global_allocator]
static GLOBAL: jemallocator::Jemalloc = jemallocator::Jemalloc;

mod cmdline;

fn main() -> anyhow::Result<()> {
    let exec_start = std::time::Instant::now();
    let args = cmdline::parse();

    utils::tracing::tracing_subscriber(args.log_filter, None)?.init();

    match args.subcommand {
        cmdline::Subcommand::HelloWorld(hello_world) => match hello_world.subcommand {
            cmdline::HelloWorldSubcommand::Greet {} => greet()
        }
    }?;

    let elapsed = exec_start.elapsed();
    tracing::info!(?elapsed, "finished execution");

    Ok(())
}


fn greet() -> anyhow::Result<()> {
    println!("Hello, world! 40 + 2 = {}", general_purpose_project_lib::add(40, 2));

    Ok(())
}
