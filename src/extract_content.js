// extract_content.js

function extractContent(element) {
    let result = [];
    let currentText = "";

    // console.log("Starting extractContent for element:", element.tagName, element.className);

    function processNode(node) {
        if (node.nodeType === Node.TEXT_NODE) {
            currentText += node.textContent;
            // console.log("Added text to currentText:", node.textContent.trim(), "Current accumulated:", currentText.trim());
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            // console.log("Processing ELEMENT_NODE:", node.tagName);

            // Only push currentText if the element is a block-level element or
            // if it's an element that should force a text push (e.g., an image)
            const blockOrForcePushTags = ['P', 'DIV', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'LI', 'UL', 'OL', 'BR', 'IMG', 'IFRAME', 'A'];

            if (blockOrForcePushTags.includes(node.tagName) && currentText.trim() !== "") {
                result.push({ type: 'text', content: currentText.trim() });
                currentText = "";
            }

            // Handle specific element types
            if (node.tagName === 'IMG') {
                const src = node.src;
                if (src && !src.startsWith('data:image/png;')) {
                    result.push({ type: 'image', url: src });
                }
            } else if (node.tagName === 'IFRAME') {
                const src = node.src;
                if (src && /(youtube\.com\/embed\/|youtube-nocookie\.com\/embed\/|www\.youtube\.com\/watch\?v=|youtu\.be\/)/.test(src)) {
                    result.push({ type: 'youtube', url: src });
                }
            } else if (node.tagName === 'A') {
                const href = node.href;
                if (href && /(youtube\.com\/watch\?v=|youtu\.be\/)/.test(href)) {
                    result.push({ type: 'youtube_link', url: href, text: node.textContent.trim() });
                }
            }

            // Recurse for children
            for (const child of node.childNodes) {
                processNode(child);
            }

            // After processing children, if it's a block-level tag, push any remaining text
            // accumulated within this block and reset.
            const blockTags = ['P', 'DIV', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'LI', 'UL', 'OL', 'BR'];
            if (blockTags.includes(node.tagName) && currentText.trim() !== "") {
                result.push({ type: 'text', content: currentText.trim() });
                currentText = "";
            }
        }
    }

    // Start processing from the element's child nodes
    for (const child of element.childNodes) {
        processNode(child);
    }

    // After processing all nodes, push any remaining accumulated text
    if (currentText.trim() !== "") {
        result.push({ type: 'text', content: currentText.trim() });
    }

    // console.log("Finished extractContent, final result length:", result.length);
    return result;
}