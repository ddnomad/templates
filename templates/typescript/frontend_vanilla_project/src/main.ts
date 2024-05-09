import { createElement } from "./utils/dom.ts";
import logger from "./utils/logging.ts";
import styles from "./main.module.scss";


function main() {
    logger.info(`Creating application root: elementId="${styles.root}"`);
    const rootDiv = createElement("div", styles.root);
    rootDiv.textContent = "Hello, world!";
}


main();
