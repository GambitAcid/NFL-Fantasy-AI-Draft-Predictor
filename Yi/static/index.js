playerList = []
playerListDisplay = []
userRoster = []

// called by player dropdown
function playerSelected() {
  let dropdownMenu = d3.select("#selectPlayer");
  let player = dropdownMenu.property("value");
  console.log("selected player is " + player)
}

function addSelectedPlayer(player) {
  // console.log("addTickerSelected being executed on " + ticker)
  d3.select("#userRoster")
    .append("button")
    .html(player)
    .attr("class", "player")
    .on("click", function (d) {
      console.log(d.target.childNodes[0].data);
      console.log(searchPlayerList((d.target.childNodes[0].data).split(",")[0]))
    })
}

init();

function init() {

  // selectPlayerCard
  d3.json("/players/names").then(function (response) {
    console.log("/players/names");
    console.log(response);
    // response = response.sort()

    for (var i = 0; i < response.length; i++) {
      var obj = response[i]
      d3.select('#selectPlayer')
        .append('option')
        .text(obj.player)
    }
  })

  d3.json("/players/all").then(function (response) {
    // console.log("/players/all");
    // console.log(response);
    playerList = response
    filterBuildTableClean("All")
    handlePagination()
  })

  // displaying radius chart
  drawRadialChart('All')
  console.log("display radial chart")


}//end init

//utility
function resetLines() {
  // console.log("resetlines executing")
  d3.select('#userRoster').selectAll("*").remove()
  tickerData = []
}

//takes a player name and searches list of players for player data
function searchPlayerList(player) {
  for (var i = 0; i < playerList.length; i++) {
    var obj = playerList[i]
    if (player === obj.player) {
      return obj
    }
  }
}

function filterBuildTableClean(pos) {
  d3.select('#playerTable').select('tbody').selectAll("*").remove()
  playerListDisplay = []

  for (var i = 0; i < playerList.length; i++) {
    var obj = playerList[i]
    if (pos === "All" || obj.pos === pos) {

      row = d3.select('#playerTable').select('tbody').append("tr")
      // .data(obj)
      // .enter().append("tr")
      row.append('td').text(obj.player)
      row.append('td').text(obj.points2021)
      row.append('td').text(obj.pos)
      row.append('td').text(obj.production.toFixed(3))
      row.append('td').text(obj.atp.toFixed(3))
      row.append('td').text(obj.team)
      row.append('td').text(obj.avg)
      row.append('td').text(obj.pred.toFixed(3))
      row.append('td').append("button").attr("value", obj.player).text("+").on("click", function (d) {
        console.log(d.target.value)
        addSelectedPlayer((d.target.value))
      })
      playerListDisplay.push(obj)
    }
  }
}

function handlePagination() {
  d3.select('#nav').selectAll("*").remove()

  $(document).ready(function () {
    $('#playerTable').after('<div id="nav"></div>');
    var rowsShown = 10;
    var rowsTotal = $('#playerTable tbody tr').length;
    var numPages = rowsTotal / rowsShown;
    for (i = 0; i < numPages; i++) {
      var pageNum = i + 1;
      $('#nav').append('<a href="#" rel="' + i + '">' + pageNum + '</a> ');
    }
    $('#playerTable tbody tr').hide();
    $('#playerTable tbody tr').slice(0, rowsShown).show();
    $('#nav a:first').addClass('active');
    $('#nav a').bind('click', function () {

      $('#nav a').removeClass('active');
      $(this).addClass('active');
      var currPage = $(this).attr('rel');
      var startItem = currPage * rowsShown;
      var endItem = startItem + rowsShown;
      $('#playerTable tbody tr').css('opacity', '0.0').hide().slice(startItem, endItem).
        css('display', 'table-row').animate({ opacity: 1 }, 300);
    })
  })
}
// drawing the radial chart

function drawRadialChart(pos) {
  console.log('draw radial chart is working?')
  // set the dimensions and margins of the graph
  const margin = { top: 0, right: 0, bottom: 0, left: -250 },
    width = 1500 - margin.left - margin.right,
    height = 1500 - margin.top - margin.bottom,
    innerRadius = 350,
    outerRadius = Math.min(width, height) / 2.5;   // the outerRadius goes from the middle of the SVG area to the border

  // append the svg object
  const svg = d3.select("#radialChart")
    .html("")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${width / 2 + margin.left}, ${height / 2 + margin.top})`);

  // accessing player data
  d3.json("/players/all").then(function (data) {
    // d3.json("/draft").then(function (data) {
    // console.log("draft response")
    // console.log(data)

    if (pos != 'All') {
      data = data.filter(d => { return d.pos == pos })
    }
    //sort
    data = data.sort((a, b) => { return b.pred - a.pred })

    // Scales
    const x = d3.scaleBand()
      .range([0, 2 * Math.PI])    // X axis goes from 0 to 2pi = all around the circle. If I stop at 1Pi, it will be around a half circle
      .align(0)                  // This does nothing
      .domain(data.map(d => d.player)); // The domain of the X axis is the list of states.
    const y = d3.scaleRadial()
      .range([innerRadius, outerRadius])   // Domain will be define later.
      .domain([0, 14000]); // Domain of Y is from 0 to the max seen in the data

    // Add the bars
    svg.append("g")
      .selectAll("path")
      .data(data)
      .join("path")
      .attr("fill", "#ffce1b")
      .attr("d", d3.arc()     // imagine your doing a part of a donut plot
        .innerRadius(innerRadius)
        .outerRadius(d => y(15 * d['pred']))
        .startAngle(d => x(d.player))
        .endAngle(d => x(d.player) + x.bandwidth())
        .padAngle(0.01)
        .padRadius(innerRadius))

    // Add the labels
    svg.append("g")
      .selectAll("g")
      .data(data)
      .join("g")
      .attr("text-anchor", function (d) { return (x(d.player) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "end" : "start"; })
      .attr("transform", function (d) { return "rotate(" + ((x(d.player) + x.bandwidth() / 2) * 180 / Math.PI - 90) + ")" + "translate(" + (y(d['pred']) + 90) + ",0)"; })
      .append("text")
      .text(function (d) { return (`${d.player}: ${d.avg}`) })
      .attr("transform", function (d) { return (x(d.player) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "rotate(180)" : "rotate(0)"; })
      .style("font-size", "11px")
      .attr("alignment-baseline", "middle")

    console.log("confirm chart is graphed")
  })
};

// function to update all the charts 
function updateAllCharts(pos) {
  filterBuildTableClean(pos)
  handlePagination()
  drawRadialChart(pos)

  console.log("confirm updating all charts")
}