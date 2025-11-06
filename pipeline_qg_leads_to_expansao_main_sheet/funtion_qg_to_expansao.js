function exportarLeadsParaPlanilhaOficial() {
  const idInput = "1VpJy5iZtLAILI9L6XIvjW6VDYE9T36mLnS7GmzFKoUk";
  const idOutput = "1rVSFAF0WQnopDYjnlBqG9HOkmrnXaYnyBhuLwWAIFXQ";
  const abaInput = "leads"; // ajuste se necessário

  const BATCH_SIZE = 100;

  const ssInput = SpreadsheetApp.openById(idInput);
  const sheetInput = ssInput.getSheetByName(abaInput);
  const dataInput = sheetInput.getDataRange().getValues();
  const ssOutput = SpreadsheetApp.openById(idOutput);

  // mapa DDD -> responsável (fixos)
  const responsaveis = {
    "GONÇALVES": [82,96,92,97,71,73,74,75,77,85,88,98,99,91,93,94,83,81,87,86,89,84,95,79,63],
    "MAGRINI": [68,65,66,67,31,32,33,34,35,37,38,69],
    "HEDER": [61,62,64,41,42,43,44,45,46,51,53,54,55,47,48,49],
    "JHONNY": [27,28,21,22,24],
    // ⚠️ DDDs 11–19 serão tratados de forma especial abaixo
  };

  // grupo que divide SP (11–19)
  const grupoSP = ["UNGARO", "MURALHA", "VICTÃO", "JULIÃO", "KATCHAU"];
  const contadorSP = {}; // usado para distribuir igualmente
  grupoSP.forEach(nome => contadorSP[nome] = 0);

  // nomes aceitos na coluna "QUEM PEGOU?"
  const nomesValidados = {
    "JHONNY": "JHONY",
    "UNGARO": "UNGARO",
    "GONÇALVES": "GONÇALVES",
    "MAGRINI": "MAGRINI",
    "HEDER": "HEDER",
    "MURALHA": "DIGÃO",
    "VICTÃO": "VICTÃO",
    "JULIÃO": "JULIÃO",
    "KATCHAU": "KATCHAU"
  };

  // helpers
  function formatarTelefone(num) {
    if (!num) return "";
    let digits = num.toString().replace(/\D/g, "");
    if (digits.startsWith("55")) digits = digits.substring(2);
    if (digits.length === 10) return `55 (${digits.substring(0,2)}) ${digits.substring(2,6)}-${digits.substring(6)}`;
    if (digits.length === 11) return `55 (${digits.substring(0,2)}) ${digits.substring(2,7)}-${digits.substring(7)}`;
    return `55 (${digits.substring(0,2)}) ${digits.substring(2)}`;
  }

  function addDias(dateStr, dias=4) {
    if (!dateStr) return "";
    const d = new Date(dateStr);
    d.setDate(d.getDate() + dias);
    return Utilities.formatDate(d, Session.getScriptTimeZone(), "dd/MM/yyyy");
  }

  function obterUF(ddd) {
    const mapaUF = {
      82:"AL",96:"AP",92:"AM",97:"AM",71:"BA",73:"BA",74:"BA",75:"BA",77:"BA",
      85:"CE",88:"CE",98:"MA",99:"MA",91:"PA",93:"PA",94:"PA",83:"PB",81:"PE",
      87:"PE",86:"PI",89:"PI",84:"RN",95:"RR",79:"SE",63:"TO",68:"AC",65:"MT",
      66:"MT",67:"MS",31:"MG",32:"MG",33:"MG",34:"MG",35:"MG",37:"MG",38:"MG",
      69:"RO",61:"DF",62:"GO",64:"GO",41:"PR",42:"PR",43:"PR",44:"PR",45:"PR",
      46:"PR",51:"RS",53:"RS",54:"RS",55:"RS",47:"SC",48:"SC",49:"SC",
      27:"ES",28:"ES",21:"RJ",22:"RJ",24:"RJ",12:"SP",13:"SP",14:"SP",15:"SP",
      16:"SP",17:"SP",18:"SP",19:"SP",11:"SP"
    };
    return mapaUF[ddd] || "";
  }

  // colunas
  const colNome = 0;
  const colTelefone = 1;
  const colDDD = 2;
  const colData = 3;
  const colNomeWhats = 4;
  const colRegiao = 5;
  const colEtiqueta = 6;
  const colStatus = 7;

  const pendentes = [];
  for (let i = 1; i < dataInput.length; i++) {
    const status = dataInput[i][colStatus];
    if (!status) pendentes.push({i, linha: dataInput[i]});
    if (pendentes.length >= BATCH_SIZE) break;
  }
  if (pendentes.length === 0) {
    Logger.log("⏸ Nenhum registro pendente. Nada a processar.");
    return;
  }

  const rowsBySheet = {};
  const sheetsCache = {};
  const dataEnvio = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "dd/MM/yyyy");
  let totalInseridos = 0;

  for (const item of pendentes) {
    const i = item.i;
    const linha = item.linha;

    const nome = linha[colNome] || linha[colNomeWhats] || "";
    const telefone = linha[colTelefone];
    const ddd = parseInt(linha[colDDD]);
    const dataInscricao = linha[colData];
    const regiao = linha[colRegiao];
    const etiqueta = linha[colEtiqueta];
    const fonte = (etiqueta && etiqueta.toUpperCase().trim() === "VINDO DO QG") ? "QG" : "";

    let responsavel = null;

    // ⚙️ Se o DDD for entre 11 e 19 → distribuir igualmente entre os 5
    if (ddd >= 11 && ddd <= 19) {
      // encontrar quem tem menos leads até agora
      const proximo = Object.entries(contadorSP).sort((a, b) => a[1] - b[1])[0][0];
      responsavel = proximo;
      contadorSP[responsavel]++;
    } else {
      // segue mapeamento fixo
      for (const r in responsaveis) {
        if (responsaveis[r].includes(ddd)) { responsavel = r; break; }
      }
    }

    if (!responsavel) {
      Logger.log(`⚠️ DDD não mapeado (linha ${i+1}): ${ddd}`);
      sheetInput.getRange(i+1, colStatus+1).setValue("DDD_NAO_MAPEADO");
      continue;
    }

    if (!sheetsCache[responsavel]) {
      const sh = ssOutput.getSheetByName(responsavel);
      if (!sh) {
        Logger.log(`❌ Aba destino não existe: ${responsavel} (linha ${i+1})`);
        sheetInput.getRange(i+1, colStatus+1).setValue("ABA_NAO_ENCONTRADA");
        continue;
      }
      sheetsCache[responsavel] = sh;
      rowsBySheet[responsavel] = [];
    }

    const telefoneFormatado = formatarTelefone(telefone);
    const prazo = addDias(dataInscricao);
    const nomeValidado = nomesValidados[responsavel] || responsavel;

    const rowToInsert = [
      null,
      nome,
      telefoneFormatado,
      regiao || "",
      obterUF(ddd) || "",
      fonte,
      dataInscricao || "",
      prazo || "",
      nomeValidado,
      "", "", "", "", ""
    ];

    rowsBySheet[responsavel].push({row: rowToInsert, inputRowIndex: i});
  }

  // gravação em bloco
  for (const responsavel in rowsBySheet) {
    const entries = rowsBySheet[responsavel];
    if (!entries.length) continue;
    const sh = sheetsCache[responsavel];
    const lastRow = sh.getLastRow();
    let startNum = Math.max(1, lastRow);
    const values = entries.map((e, idx) => {
      const seq = startNum + idx;
      e.row[0] = seq - 1;
      return e.row;
    });
    sh.getRange(lastRow + 1, 1, values.length, values[0].length).setValues(values);
    totalInseridos += values.length;

    for (const e of entries) {
      const inputIndex = e.inputRowIndex;
      sheetInput.getRange(inputIndex + 1, colStatus + 1).setValue(dataEnvio);
    }
  }

  Logger.log(`✅ Exportados: ${totalInseridos}. Distribuição SP: ${JSON.stringify(contadorSP)}`);
}
