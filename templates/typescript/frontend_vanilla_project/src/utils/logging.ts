import chalk from "chalk";


function log(message: string): void {
    console.log(`${chalk.blue(message)}`);
}


const logger = {
    info: log,
    "error": log
};


export default logger;
