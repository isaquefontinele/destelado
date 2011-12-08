$(function() {
    $("table").tablesorter({ 
        textExtraction: function(node) {
            switch(node.className) {
                case "name":
                    return node.childNodes[0].textContent;
                case "frequency":
                    textContent = node.textContent;
                    frequency = node.textContent.substring(8, textContent.length-1).split(" / ");
                    return parseInt(frequency[0]) / parseInt(frequency[1]);
                default:
                    return node.innerHTML;
            }
        } 
    });
});