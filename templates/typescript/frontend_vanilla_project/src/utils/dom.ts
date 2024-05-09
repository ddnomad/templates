import logger from "./logging.ts";


export function createElement(type: string, id: string, parent: HTMLElement = document.body): HTMLElement {
    logger.info(`Creating HTML element: type="${type}" id="${id}" parent="${parent.nodeName}"`);
    const element = document.createElement(type);

    element.id = id;
    parent.appendChild(element);

    return element;
}
