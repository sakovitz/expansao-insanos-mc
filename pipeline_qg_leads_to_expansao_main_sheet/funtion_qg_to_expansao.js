/**
 * exportarLeadsParaPlanilhaOficial()
 *
 * Este script automatiza a exportação de leads de uma planilha de entrada ("leads")
 * para uma planilha oficial de destino, dividindo os registros conforme DDD.
 * 
 * - Lê até BATCH_SIZE registros ainda não processados (sem status)
 * - Atribui responsável conforme o DDD
 * - Formata e insere as informações na aba do responsável
 * - Atualiza o status da linha original com a data de envio
 * 
 * Configurado para execução automática a cada hora.
 */

function exportarLeadsParaPlanilhaOficial() {
  // === CONFIGURAÇÕES PRINCIPAIS ===
  const idInput = "1VpJy5iZtLAILI9L6XIvjW6VDYE9T36mLnS7GmzFKoUk";  // Planilha de entrada (leads)
  const idOutput = "1rVSFAF0WQnopDYjnlBqG9HOkmrnXaYnyBhuLwWAIFXQ"; // Planilha destino (oficial)
  const abaInput = "leads"; // Nome da aba de origem
  const BATCH_SIZE = 100;   // Máximo de leads processados por execução

  // === ACESSO ÀS PLANILHAS ===
  const ssInput = SpreadsheetApp.openById(idInput);
  const sheetInput = ssInput.getSheetByName(abaInput);
  const dataInput = sheetInput.getDataRange().getValues(); // Carrega todos os dados
  const ssOutput = SpreadsheetApp.openById(idOutput);

  // === MAPEAMENTO FIXO DE RESPONSÁVEIS POR DDD ===
  const responsaveis = {
    "GONÇALVES": [82,96,92,97,71,73,74,75,77,85,88,98,99,91,93,94,83,81,87,86,89,84,95,79,63],
    "MAGRINI":   [68,65,66,67,31,32,33,34,35,37,38,69],
    "HEDER":     [61,62,64,41,42,43,44,45,46,51,53,54,55,47,48,49],
    "JHONNY":    [27,28,21,22,24],
    // DDDs 11–19 são tratados separadamente (grupo SP)
  };

  // === GRUPO ESPECIAL: DISTRIBUIÇÃO IGUAL ENTRE 5 RESPONSÁVEIS ===
  const grupoSP = ["UNGARO", "MURALHA", "VICTÃO", "JULIÃO", "KATCHAU"];
  const contadorSP = {}; // Contador de leads por pessoa (para divisão balanceada)
  grupoSP.forEach(nome => contadorSP[nome] = 0);

  // === PADRONIZAÇÃO DE NOMES PARA A COLUNA “QUEM PEGOU?” ===
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

  // === FUNÇÕES AUXILIARES ===

  /** 
   * Formata número de telefone para padrão "55 (DD) 9XXXX-XXXX"
   */
  function formatarTelefone(num) {
    if (!num) return "";
    let digits = num.toString().replace(/\D/g, ""); // Remove caracteres não numéricos
    if (digits.startsWith("55")) digits = digits.substring(2);
    if (digits.length === 10) return `55 (${digits.substring(0,2)}) ${digits.substring(2,6)}-${digits.substring(6)}`;
    if (digits.length === 11) return `55 (${digits.substring(0,2)}) ${digits.substring(2,7)}-${digits.substring(7)}`;
    return `55 (${digits.substring(0,2)}) ${digits.substring(2)}`;
  }

  /**
   * Soma X dias a uma data e retorna no formato dd/MM/yyyy.
   * Usado para calcular o prazo padrão (4 dias após inscrição)
   */
  function addDias(dateStr, dias=4) {
    if (!dateStr) return "";
    const d = new Date(dateStr);
    d.setDate(d.getDate() + dias);
    return Utilities.formatDate(d, Session.getScriptTimeZone(), "dd/MM/yyyy");
  }

  /**
   * Retorna a UF (estado) correspondente ao DDD.
   */
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

  // === DEFINIÇÃO DOS ÍNDICES DAS COLUNAS ===
  const colNome = 0;
  const colTelefone = 1;
  const colDDD = 2;
  const colData = 3;
  const colNomeWhats = 4;
  const colRegiao = 5;
  const colEtiqueta = 6;
  const colStatus = 7;

  // === SELECIONA REGISTROS PENDENTES ===
  const pendentes = [];
  for (let i = 1; i < dataInput.length; i++) {
    const status = dataInput[i][colStatus];
    if (!status) pendentes.push({i, linha: dataInput[i]});
    if (pendentes.length >= BATCH_SIZE) break; // limita lote
  }

  if (pendentes.length === 0) {
    Logger.log("⏸ Nenhum registro pendente. Nada a processar.");
    return;
  }

  // === ESTRUTURAS TEMPORÁRIAS PARA PROCESSAMENTO ===
  const rowsBySheet = {};   // Armazena as linhas por aba de destino
  const sheetsCache = {};   // Cache de abas já abertas
  const dataEnvio = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "dd/MM/yyyy");
  let totalInseridos = 0;

  // === LOOP PRINCIPAL: PROCESSAMENTO DOS LEADS ===
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

    // === REGRA ESPECIAL: DDDs 11–19 (grupo SP) ===
    if (ddd >= 11 && ddd <= 19) {
      // Distribui para quem tem menos leads até o momento
      const proximo = Object.entries(contadorSP).sort((a, b) => a[1] - b[1])[0][0];
      responsavel = proximo;
      contadorSP[responsavel]++;
    } else {
      // Demais DDDs seguem o mapeamento fixo
      for (const r in responsaveis) {
        if (responsaveis[r].includes(ddd)) { 
          responsavel = r; 
          break; 
        }
      }
    }

    // === CASOS DE ERRO ===
    if (!responsavel) {
      Logger.log(`⚠️ DDD não mapeado (linha ${i+1}): ${ddd}`);
      sheetInput.getRange(i+1, colStatus+1).setValue("DDD_NAO_MAPEADO");
      continue;
    }

    // === CACHE DE ABA ===
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

    // === PREPARAÇÃO DOS DADOS PARA INSERÇÃO ===
    const telefoneFormatado = formatarTelefone(telefone);
    const prazo = addDias(dataInscricao);
    const nomeValidado = nomesValidados[responsavel] || responsavel;

    const rowToInsert = [
      null, // Número sequencial (preenchido depois)
      nome,
      telefoneFormatado,
      regiao || "",
      obterUF(ddd) || "",
      fonte,
      dataInscricao || "",
      prazo || "",
      nomeValidado,
      "", "", "", "", "" // colunas extras (reservadas)
    ];

    rowsBySheet[responsavel].push({row: rowToInsert, inputRowIndex: i});
  }

  // === INSERÇÃO EM BLOCO NAS PLANILHAS DE DESTINO ===
  for (const responsavel in rowsBySheet) {
    const entries = rowsBySheet[responsavel];
    if (!entries.length) continue;

    const sh = sheetsCache[responsavel];
    const lastRow = sh.getLastRow();
    
    // Determina sequência a partir do último número da coluna A
    let startNum = Math.max(1, lastRow);

    const values = entries.map((e, idx) => {
      const seq = startNum + idx;
      e.row[0] = seq - 1; // Coluna A = número sequencial
      return e.row;
    });

    // Grava linhas no final da aba
    sh.getRange(lastRow + 1, 1, values.length, values[0].length).setValues(values);
    totalInseridos += values.length;

    // Atualiza status da planilha de entrada com data de envio
    for (const e of entries) {
      const inputIndex = e.inputRowIndex;
      sheetInput.getRange(inputIndex + 1, colStatus + 1).setValue(dataEnvio);
    }
  }

  Logger.log(`✅ Exportados: ${totalInseridos}. Distribuição SP: ${JSON.stringify(contadorSP)}`);
}
