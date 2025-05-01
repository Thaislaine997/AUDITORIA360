function inserirDadosNaMatriz(empresa, cnpj, piso, he, adicional) {
  var planilha = SpreadsheetApp.openById("ID_DA_PLANILHA_MATRIZ");
  var aba = planilha.getSheetByName("Base");
  var ultimaLinha = aba.getLastRow() + 1;

  aba.getRange(ultimaLinha, 1).setValue(empresa);
  aba.getRange(ultimaLinha, 2).setValue(cnpj);
  aba.getRange(ultimaLinha, 3).setValue(piso);
  aba.getRange(ultimaLinha, 4).setValue(he);
  aba.getRange(ultimaLinha, 5).setValue(adicional);

  return "Inserido com sucesso na planilha matriz!";
}
