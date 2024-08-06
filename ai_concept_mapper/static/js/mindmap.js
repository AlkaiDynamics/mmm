// static/js/mindmap.js

// Ensure the document is fully loaded before executing any script
document.addEventListener('DOMContentLoaded', function () {
    // Initialize the SVG canvas for the mind map
    const width = 960;
    const height = 600;
    const svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

    // Define the force simulation
    const simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(d => d.id))
        .force("charge", d3.forceManyBody().strength(-400))
        .force("center", d3.forceCenter(width / 2, height / 2));

    // Load the initial data from the server
    d3.json("/load_ontology").then(function (data) {
        const nodes = Object.keys(data.concepts).map(concept => ({ id: concept }));
        const links = []; // Initialize an empty array for links

        // Render the mind map
        renderMindMap(nodes, links);
    });

    // Function to render the mind map
    function renderMindMap(nodes, links) {
        // Remove any existing elements
        svg.selectAll("*").remove();

        // Create link elements
        const link = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(links)
            .enter().append("line")
            .attr("stroke-width", 2);

        // Create node elements
        const node = svg.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(nodes)
            .enter().append("circle")
            .attr("r", 10)
            .attr("fill", "blue")
            .call(d3.drag()
                .on("start", dragStarted)
                .on("drag", dragged)
                .on("end", dragEnded));

        // Add labels to nodes
        const label = svg.append("g")
            .attr("class", "labels")
            .selectAll("text")
            .data(nodes)
            .enter().append("text")
            .attr("dy", -15)
            .attr("dx", 15)
            .text(d => d.id);

        // Update the simulation with nodes and links
        simulation
            .nodes(nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(links);

        // Function to update positions on each tick
        function ticked() {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);

            label
                .attr("x", d => d.x)
                .attr("y", d => d.y);
        }
    }

    // Functions to handle drag events
    function dragStarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragEnded(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    // Function to add a node
    function addNode(concept, data) {
        const newNode = { id: concept };
        nodes.push(newNode);
        renderMindMap(nodes, links);
    }

    // Function to remove a node
    function removeNode(concept) {
        const index = nodes.findIndex(node => node.id === concept);
        if (index !== -1) {
            nodes.splice(index, 1);
            renderMindMap(nodes, links);
        }
    }

    // Expose functions to the global scope for external access
    window.addNode = addNode;
    window.removeNode = removeNode;
});
