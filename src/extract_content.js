function extractContent(element) {
    let result = [];
    
    // Process all child nodes recursively
    function processNode(node) {
        if (node.nodeType === Node.TEXT_NODE) {
            const text = node.textContent.trim();
            if (text) result.push({ type: 'text', content: text });
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            // Handle images
            if (node.tagName === 'IMG') {
                const src = node.src;
                if (src && !src.startsWith('data:image/png;')) {
                    result.push({ type: 'image', url: src });
                }
            }
            // Handle iframes (YouTube embeds)
            else if (node.tagName === 'IFRAME') {
                const src = node.src;
                if (src && (src.includes('youtube.com') || src.includes('youtu.be'))) {
                    result.push({ type: 'youtube', url: src });
                }
            }
            // Handle links to YouTube
            else if (node.tagName === 'A') {
                const href = node.href;
                if (href && (href.includes('youtube.com') || href.includes('youtu.be'))) {
                    result.push({ type: 'youtube_link', url: href, text: node.textContent.trim() });
                }
            }
            // Process children recursively
            for (const child of node.childNodes) {
                processNode(child);
            }
        }
    }
    
    // Start processing from the element
    for (const child of element.childNodes) {
        processNode(child);
    }
    
    return result;
}