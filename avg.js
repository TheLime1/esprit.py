function tableToJson(table) {
  var data = [];

  // first row needs to be headers
  var headers = [];
  for (var i = 0; i < table.rows[0].cells.length; i++) {
    headers[i] = table.rows[0].cells[i].innerHTML
      .toLowerCase()
      .replace(/ /gi, "");
  }

  // go through cells
  for (var i = 1; i < table.rows.length; i++) {
    var tableRow = table.rows[i];
    var rowData = {};

    for (var j = 0; j < tableRow.cells.length; j++) {
      rowData[headers[j]] = tableRow.cells[j].innerHTML;
    }
    data.push(rowData);
  }

  data.forEach((x) => {
    if (x.coef) x.coef = parseFloat(x.coef.replace(",", "."));
    if (x.note_cc) x.note_cc = parseFloat(x.note_cc.replace(",", "."));
    if (x.note_tp) x.note_tp = parseFloat(x.note_tp.replace(",", "."));
    if (x.note_exam) x.note_exam = parseFloat(x.note_exam.replace(",", "."));
  });
  return data;
}

var table = document.getElementById("ContentPlaceHolder1_GridView1");

var data = tableToJson(table);

var sumCoef = 0;

data.forEach((e) => (sumCoef += e.coef));

function calculMoyenne(dataS, coefS) {
  var total = 0;
  var moyMat = [];
  dataS.forEach((x) => {
    if (isNaN(x.note_tp)) {
      if (isNaN(x.note_cc)) {
        x.moyenne = x.note_exam;
        total += x.note_exam * x.coef;
      } else {
        x.moyenne = x.note_exam * 0.6 + x.note_cc * 0.4;
        moyMat.push(x.note_exam * 0.6 + x.note_cc * 0.4);
        total += (x.note_exam * 0.6 + x.note_cc * 0.4) * x.coef;
      }
    } else if (isNaN(x.note_cc)) {
      x.moyenne = x.note_exam * 0.8 + x.note_tp * 0.2;
      moyMat.push(x.note_exam * 0.8 + x.note_tp * 0.2);
      total += (x.note_exam * 0.8 + x.note_tp * 0.2) * x.coef;
    } else {
      x.moyenne = x.note_exam * 0.5 + x.note_cc * 0.3 + x.note_tp * 0.2;
      moyMat.push(x.note_exam * 0.5 + x.note_cc * 0.3 + x.note_tp * 0.2);
      total += (x.note_exam * 0.5 + x.note_cc * 0.3 + x.note_tp * 0.2) * x.coef;
    }
  });
  dataS.push({
    designation: "Moyenne",
    coef: coefS,
    nom_ens: "",
    note_cc: "",
    note_tp: "",
    note_exam: "",
    moyenne: total / coefS,
  });
  return dataS;
}

var newData = calculMoyenne(data, sumCoef);

function populateTable(data) {
  // Empty content string
  var tableContent =
    '<tr style="color:White;background-color:#A80000;font-weight:bold;"> <th scope="col">DESIGNATION</th><th scope="col">COEF</th><th scope="col">NOM_ENS</th><th scope="col">NOTE_CC</th><th scope="col">NOTE_TP</th><th scope="col">NOTE_EXAM</th><th scope="col">Moyenne</th></tr>';

  data.forEach((x) => {
    tableContent += "<tr>";
    tableContent += "<td>" + x.designation + "</td>";
    tableContent += "<td>" + x.coef + "</td>";
    tableContent += "<td>" + x.nom_ens + "</td>";
    tableContent += isNaN(x.note_cc)
      ? "<td></td>"
      : "<td>" + x.note_cc + "</td>";
    tableContent += isNaN(x.note_tp)
      ? "<td></td>"
      : "<td>" + x.note_tp + "</td>";
    tableContent += isNaN(x.note_exam)
      ? "<td></td>"
      : "<td>" + x.note_exam + "</td>";
    tableContent += x.moyenne
      ? x.moyenne > 8
        ? '<td style="background-color:green">' + x.moyenne.toFixed(2) + "</td>"
        : '<td style="background-color:red">' + x.moyenne.toFixed(2) + "</td>"
      : "<td></td>";
    tableContent += "</tr>";
  });
  $("#ContentPlaceHolder1_GridView1 tbody").html(tableContent);
}

populateTable(newData);
