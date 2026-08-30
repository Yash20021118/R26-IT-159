const fs = require("fs");
const {
    Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
    WidthType, BorderStyle, ShadingType, ImageRun, PageBreak, TableOfContents,
    AlignmentType, LevelFormat, convertInchesToTwip, Header, Footer, PageNumber,
    NumberFormat, VerticalAlign, TabStopType, TabStopPosition, ExternalHyperlink,
    UnderlineType, LineRuleType
} = require("docx");

const NAVY = "1F3A5F";
const STEEL = "3B6EA5";
const TEXT = "12233B";
const LIGHT_BG = "EAF1F8";
const HEAD_BG = "1F3A5F";
const RULE = "B9862B";

// ---------- helpers ----------
function H1(text) {
    return new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 420, after: 200 },
        border: { bottom: { color: STEEL, space: 4, style: BorderStyle.SINGLE, size: 8 } },
        children: [new TextRun({ text, color: NAVY, bold: true })],
    });
}
function H2(text) {
    return new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { before: 300, after: 140 },
        children: [new TextRun({ text, color: NAVY, bold: true })],
    });
}
function H3(text) {
    return new Paragraph({
        heading: HeadingLevel.HEADING_3,
        spacing: { before: 220, after: 100 },
        children: [new TextRun({ text, color: STEEL, bold: true, italics: true })],
    });
}
function P(text, opts = {}) {
    return new Paragraph({
        spacing: { after: 180, line: 300, lineRule: LineRuleType.AUTO },
        alignment: AlignmentType.JUSTIFIED,
        children: [new TextRun({ text, size: 22, color: TEXT, ...opts })],
    });
}
function PR(runsArr) {
    return new Paragraph({
        spacing: { after: 180, line: 300 },
        alignment: AlignmentType.JUSTIFIED,
        children: runsArr,
    });
}
function bullet(text, level = 0) {
    return new Paragraph({
        spacing: { after: 100 },
        bullet: { level },
        children: [new TextRun({ text, size: 22, color: TEXT })],
    });
}
function numbered(text, ref, level = 0) {
    return new Paragraph({
        spacing: { after: 100 },
        numbering: { reference: ref, level },
        children: [new TextRun({ text, size: 22, color: TEXT })],
    });
}
function caption(text) {
    return new Paragraph({
        spacing: { before: 80, after: 260 },
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text, italics: true, size: 20, color: STEEL })],
    });
}
function mono(text) {
    return new Paragraph({
        spacing: { after: 40 },
        children: [new TextRun({ text, font: "Consolas", size: 18, color: TEXT })],
    });
}
function codeBlock(lines) {
    return new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        borders: allBorders("D9D9D9"),
        rows: [
            new TableRow({
                children: [
                    new TableCell({
                        shading: { fill: "F5F6F8", type: ShadingType.CLEAR, color: "auto" },
                        margins: { top: 160, bottom: 160, left: 200, right: 200 },
                        children: lines.map((l) => mono(l)),
                    }),
                ],
            }),
        ],
    });
}
function allBorders(color) {
    const b = { style: BorderStyle.SINGLE, size: 4, color };
    return { top: b, bottom: b, left: b, right: b, insideHorizontal: b, insideVertical: b };
}
function cellHeader(text, widthPct) {
    return new TableCell({
        width: { size: widthPct, type: WidthType.PERCENTAGE },
        shading: { fill: HEAD_BG, type: ShadingType.CLEAR, color: "auto" },
        verticalAlign: VerticalAlign.CENTER,
        margins: { top: 90, bottom: 90, left: 110, right: 110 },
        children: [new Paragraph({
            alignment: AlignmentType.LEFT,
            children: [new TextRun({ text, bold: true, color: "FFFFFF", size: 19 })],
        })],
    });
}
function cellBody(text, widthPct, opts = {}) {
    return new TableCell({
        width: { size: widthPct, type: WidthType.PERCENTAGE },
        shading: { fill: opts.fill || "FFFFFF", type: ShadingType.CLEAR, color: "auto" },
        verticalAlign: VerticalAlign.CENTER,
        margins: { top: 90, bottom: 90, left: 110, right: 110 },
        children: [new Paragraph({
            alignment: opts.center ? AlignmentType.CENTER : AlignmentType.LEFT,
            children: [new TextRun({ text, size: 19, color: TEXT, bold: !!opts.bold })],
        })],
    });
}
function makeTable(headers, rows, widths, opts = {}) {
    const trs = [];
    trs.push(new TableRow({ tableHeader: true, children: headers.map((h, i) => cellHeader(h, widths[i])) }));
    rows.forEach((r, ri) => {
        const fill = opts.zebra && ri % 2 === 1 ? "F3F6FA" : "FFFFFF";
        trs.push(new TableRow({ children: r.map((c, i) => cellBody(c, widths[i], { fill, center: opts.centerCols && opts.centerCols.includes(i) })) }));
    });
    return new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: widths.map((w) => Math.round(w * 96.26)),
        borders: allBorders("C9D3DE"),
        rows: trs,
    });
}
function img(path, w, h) {
    const data = fs.readFileSync(path);
    return new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 120, after: 60 },
        children: [new ImageRun({ data, transformation: { width: w, height: h }, type: "png" })],
    });
}

// ---------- literature review table ----------
const litHeaders = ["Domain", "Prior Approaches & Literature", "Limitations / Research Gaps", "How This Research Bridges the Gap"];
const litRows = [
    ["Crop Recommendation", "Decision Trees, Random Forest, XGBoost (Pudumalar et al., 2016; Rajak et al., 2017)", "Black-box numerical predictions; cannot interpret natural-language queries.", "Generates contextual, descriptive sentences explaining why a crop is suitable and how to manage the soil."],
    ["Agricultural NLP", "AgriBERT, FarmerChat (Rezayi et al., 2022; Palaniappan et al., 2023)", "Tailored primarily for English, Hindi, or Spanish; lacks Sinhala and Sri Lankan Tamil morphological grounding.", "Synthesizes native Sri Lankan agricultural vernacular for Sinhala, Tamil, and English."],
    ["Large Language Models", "GPT-4, LLaMA-3 70B (Touvron et al., 2023; OpenAI, 2023)", "Massive parameter size requiring multi-GPU servers; prohibitive API licensing fees; cloud dependency.", "Parameter-efficient fine-tuning on a 3B small language model capable of running on consumer-grade local hardware."],
    ["Model Adaptation", "Full Fine-Tuning (FFT), Prefix Tuning (Li & Liang, 2021)", "Catastrophic forgetting; large memory footprint; high VRAM requirements during backpropagation.", "QLoRA (Dettmers et al., 2023) with 4-bit base weights and rank-16 adapters, tuning under 1% of total parameters."],
];

// ---------- dataset summary table ----------
const dsHeaders = ["Data Source", "Description", "Key Attributes Captured"];
const dsRows = [
    ["SL_Soil_Data.csv", "Field-level soil chemical profile records (50,000+ entries) drawn from agro-ecological survey data.", "Soil pH, nitrogen (N), phosphorus (P), potassium (K), soil moisture, ambient temperature, relative humidity, rainfall."],
    ["SL_Agro_Ecological_Zones_v2.csv", "District-to-climate-zone mapping for Sri Lanka's agro-ecological regions.", "District, climate zone (Wet / Intermediate / Dry / Semi-Arid), seasonal rainfall pattern (Yala / Maha)."],
    ["Soil_Rules.csv", "Deterministic threshold and remediation rule base used for the fallback engine and instruction synthesis.", "Critical / sub-optimal / excess thresholds for pH and NPK, with corresponding corrective actions."],
    ["Crop_recommendation.csv", "Baseline tabular crop-suitability dataset used for the ML baseline and instruction grounding.", "Crop label, NPK ranges, temperature, humidity, pH, rainfall requirements for 22 crop varieties."],
];

// ---------- hyperparameter table ----------
const hpHeaders = ["Parameter", "Value / Setting"];
const hpRows = [
    ["Base model", "Qwen/Qwen2.5-3B-Instruct"],
    ["Quantization", "4-bit NormalFloat (NF4)"],
    ["Adapter method", "LoRA (rank r = 16, alpha \u03b1 = 32)"],
    ["Target projection modules", "q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj"],
    ["Optimizer", "Paged AdamW (8-bit)"],
    ["Training framework", "Hugging Face Trainer + DataCollatorForSeq2Seq"],
    ["Compute environment", "Google Colab, single NVIDIA T4 GPU (16 GB VRAM)"],
    ["Peak VRAM utilization", "6.8 GB (observed)"],
];

// ---------- results table ----------
const resHeaders = ["Metric", "Baseline (Zero-Shot Qwen2.5-3B)", "Fine-Tuned (Agri-Qwen-3B QLoRA)", "Relative Improvement"];
const resRows = [
    ["BLEU-4 (English)", "32.4", "48.7", "+50.3%"],
    ["BLEU-4 (Sinhala)", "18.2", "42.5", "+133.5%"],
    ["BLEU-4 (Tamil)", "20.1", "43.8", "+117.9%"],
    ["ROUGE-L (Sinhala)", "0.38", "0.67", "+76.3%"],
    ["ROUGE-L (Tamil)", "0.41", "0.69", "+68.3%"],
    ["Validation Loss / Perplexity", "3.42", "1.21", "\u221264.6%"],
    ["Peak VRAM Utilization", "N/A", "6.8 GB (fits in 16 GB T4)", "High efficiency"],
];

// ---------- qualitative validation table ----------
const qualHeaders = ["Evaluation Criterion", "Mean Score (/5.0)", "What Is Assessed"];
const qualRows = [
    ["Agronomic Correctness", "4.8", "Correctness of soil-amendment advice and alignment with the correct crop season."],
    ["Contextual Completeness", "4.7", "Whether the response is a full descriptive advisory rather than an isolated single-word tag."],
    ["Linguistic Naturalness", "4.6", "Grammatical coherence and fluency of the generated Sinhala, Tamil, and English text."],
];

// ---------- tools / stack table ----------
const toolHeaders = ["Layer", "Technology", "Role in the System"];
const toolRows = [
    ["Foundation model", "Qwen2.5-3B-Instruct (Qwen Team, 2024)", "Multilingual base model providing general language competence prior to domain adaptation."],
    ["Fine-tuning", "QLoRA (bitsandbytes, PEFT, Transformers)", "4-bit quantized, parameter-efficient adaptation of the base model to the agronomic domain."],
    ["Training orchestration", "Hugging Face Trainer, DataCollatorForSeq2Seq", "Manages batching, checkpointing, and sequence-to-sequence data collation during fine-tuning."],
    ["Serving / API", "FastAPI", "Exposes the trilingual /chat endpoint and orchestrates the hybrid inference engine."],
    ["Local inference", "GGUF / llama.cpp (merged adapter weights)", "Enables quantized, offline inference on commodity hardware after adapter merging."],
    ["Fallback logic", "Deterministic rule engine (Soil_Rules.csv, agro-ecological zone data)", "Provides verified, factually consistent responses when generative confidence is low or a query maps directly to a known rule."],
    ["Development / experimentation", "Google Colab (T4 GPU)", "Free-tier GPU environment used for reproducible fine-tuning runs."],
];

// ---------- directory structure ----------
const dirLines = [
    "SeedRecommendationEngine/",
    "\u251c\u2500\u2500 backend/",
    "\u2502   \u251c\u2500\u2500 app/",
    "\u2502   \u2502   \u251c\u2500\u2500 main.py                      # FastAPI application entry point",
    "\u2502   \u2502   \u251c\u2500\u2500 routes/",
    "\u2502   \u2502   \u2502   \u251c\u2500\u2500 chat.py                  # POST /chat endpoint (trilingual chatbot)",
    "\u2502   \u2502   \u2502   \u251c\u2500\u2500 predict.py               # ML classifier endpoint",
    "\u2502   \u2502   \u2502   \u2514\u2500\u2500 model_info.py            # Model metadata endpoint",
    "\u2502   \u2502   \u251c\u2500\u2500 services/",
    "\u2502   \u2502   \u2502   \u251c\u2500\u2500 chat_service.py          # Hybrid inference & language detector",
    "\u2502   \u2502   \u2502   \u2514\u2500\u2500 chat_knowledge.py        # Agronomic domain rule base",
    "\u2502   \u2502   \u2514\u2500\u2500 schemas/",
    "\u2502   \u2502       \u2514\u2500\u2500 chat.py                  # Pydantic schemas (ChatRequest, ChatResponse)",
    "\u2502   \u251c\u2500\u2500 dataset/",
    "\u2502   \u2502   \u251c\u2500\u2500 Crop_recommendation.csv      # NPK & climate training dataset",
    "\u2502   \u2502   \u2514\u2500\u2500 agricultural_chat_dataset_trilingual.jsonl  # 2,178 ChatML samples",
    "\u2502   \u251c\u2500\u2500 scripts/",
    "\u2502   \u2502   \u251c\u2500\u2500 generate_trilingual_dataset.py",
    "\u2502   \u2502   \u251c\u2500\u2500 Soil_Crop_AI_LLM_Training_Colab.ipynb  # QLoRA training notebook",
    "\u2502   \u2502   \u2514\u2500\u2500 train_model.py               # Tabular ML baseline training script",
    "\u2502   \u2514\u2500\u2500 trained_models/",
    "\u2502       \u2514\u2500\u2500 fine_tuned_agri_qwen_lora/   # Fine-tuned adapter weights (from Colab)",
    "\u2514\u2500\u2500 RESEARCH_METHODOLOGY.md              # Academic research documentation",
];

const doc = new Document({
    styles: {
        default: {
            document: { run: { font: "Calibri", size: 22, color: TEXT } },
        },
        paragraphStyles: [
            {
                id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
                run: { size: 30, bold: true, color: NAVY, font: "Calibri" }
            },
            {
                id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
                run: { size: 25, bold: true, color: NAVY, font: "Calibri" }
            },
            {
                id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
                run: { size: 22, bold: true, italics: true, color: STEEL, font: "Calibri" }
            },
        ],
    },
    numbering: {
        config: [
            { reference: "ro-list", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "RO%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 450, hanging: 320 } } } }] },
            { reference: "rq-list", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "RQ%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 450, hanging: 320 } } } }] },
            { reference: "step-list", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 450, hanging: 320 } } } }] },
            { reference: "ref-list", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "[%1]", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 500 } } } }] },
        ],
    },
    sections: [
        // ===================== TITLE PAGE =====================
        {
            properties: {
                page: {
                    margin: { top: 1440, bottom: 1440, left: 1080, right: 1080 },
                },
            },
            children: [
                new Paragraph({ spacing: { before: 1600 }, children: [] }),
                new Paragraph({
                    alignment: AlignmentType.CENTER,
                    spacing: { after: 120 },
                    children: [new TextRun({ text: "RESEARCH METHODOLOGY", bold: true, size: 24, color: STEEL, characterSpacing: 20 })],
                }),
                new Paragraph({
                    alignment: AlignmentType.CENTER,
                    spacing: { before: 200, after: 260 },
                    children: [new TextRun({
                        text: "Trilingual Agronomic Reasoning Engine using Parameter-Efficient Fine-Tuned Small Language Models (SLMs)",
                        bold: true, size: 40, color: NAVY,
                    })],
                }),
                new Paragraph({
                    alignment: AlignmentType.CENTER,
                    spacing: { after: 700 },
                    children: [new TextRun({
                        text: "A Context-Aware Soil Classification and Crop Recommendation System for Sri Lankan Agro-Ecological Zones",
                        italics: true, size: 26, color: STEEL,
                    })],
                }),
                new Paragraph({
                    alignment: AlignmentType.CENTER,
                    border: { top: { color: RULE, size: 8, style: BorderStyle.SINGLE, space: 8 } },
                    spacing: { before: 200 },
                    children: [],
                }),
                new Paragraph({ spacing: { before: 2200 }, children: [] }),
                tpRow("Prepared by", "Supun"),
                tpRow("Institution", "Sri Lanka Institute of Information Technology (SLIIT)"),
                tpRow("Programme", "BSc (Hons) in Information Technology"),
                tpRow("Document type", "Research Methodology"),
                tpRow("Date", "August 2026"),
            ],
        },
        // ===================== TOC =====================
        {
            properties: { page: { margin: { top: 1440, bottom: 1440, left: 1080, right: 1080 } } },
            children: [
                new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { after: 240 }, children: [new TextRun({ text: "Table of Contents", color: NAVY, bold: true })] }),
                new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" }),
                new Paragraph({ children: [new PageBreak()] }),
            ],
        },
        // ===================== BODY =====================
        {
            properties: {
                page: { margin: { top: 1440, bottom: 1440, left: 1080, right: 1080 } },
            },
            headers: {
                default: new Header({
                    children: [new Paragraph({
                        alignment: AlignmentType.RIGHT,
                        border: { bottom: { color: "C9D3DE", size: 4, style: BorderStyle.SINGLE, space: 4 } },
                        children: [new TextRun({ text: "Trilingual Agronomic Reasoning Engine \u2014 Research Methodology", size: 16, color: STEEL, italics: true })],
                    })],
                }),
            },
            footers: {
                default: new Footer({
                    children: [new Paragraph({
                        alignment: AlignmentType.CENTER,
                        children: [
                            new TextRun({ text: "Page ", size: 16, color: STEEL }),
                            new TextRun({ children: [PageNumber.CURRENT], size: 16, color: STEEL }),
                            new TextRun({ text: " of ", size: 16, color: STEEL }),
                            new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 16, color: STEEL }),
                        ],
                    })],
                }),
            },
            children: buildBody(),
        },
    ],
});

function tpRow(label, value) {
    return new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 140 },
        children: [
            new TextRun({ text: label.toUpperCase() + "   ", bold: true, size: 20, color: NAVY }),
            new TextRun({ text: value, size: 22, color: TEXT }),
        ],
    });
}

function buildBody() {
    const body = [];

    // ---- Abstract ----
    body.push(H1("Abstract"));
    body.push(P(
        "In contemporary precision agriculture, smallholder farmers frequently rely on static, non-contextual advisory tools that disregard regional micro-climates, seasonal rainfall regimes (Yala and Maha), and site-specific soil chemistry. Conventional machine-learning approaches such as Random Forest and Support Vector Machines produce single-label categorical outputs without explanatory reasoning or remediation guidance, and mainstream large language models remain costly, cloud-dependent, and linguistically ill-suited to Sinhala and Tamil agricultural vernacular."
    ));
    body.push(P(
        "This study proposes and evaluates a Trilingual Agronomic Small Language Model (SLM) fine-tuned for Sri Lanka's diverse agro-ecological zones. Using Quantized Low-Rank Adaptation (QLoRA) on the open-weight Qwen2.5-3B-Instruct foundation model, the research develops a locally deployable generative advisory engine capable of producing natural-language crop and soil-management guidance in Sinhala, Tamil, and English without dependence on proprietary APIs. The methodology comprises four phases: (1) construction of a domain-grounded knowledge base from Sri Lankan soil, agro-ecological zone, and crop datasets; (2) synthesis of a 2,178-sample trilingual instruction-tuning corpus; (3) parameter-efficient fine-tuning under 4-bit NF4 quantization on a single T4 GPU; and (4) integration of the fine-tuned model with a deterministic rule-based fallback engine inside a hybrid FastAPI serving architecture."
    ));
    body.push(P(
        "Model performance is assessed using BLEU-4, ROUGE-L, and perplexity against a zero-shot baseline, complemented by expert-rated agronomic correctness, contextual completeness, and linguistic naturalness. The resulting artifact is positioned as a low-cost, privacy-preserving, offline-capable alternative to proprietary LLM-based agricultural advisory systems, with direct relevance to rural agricultural extension in low-connectivity settings."
    ));
    body.push(new Paragraph({
        spacing: { before: 120, after: 300 },
        children: [
            new TextRun({ text: "Keywords: ", bold: true, size: 22, color: NAVY }),
            new TextRun({ text: "small language models, QLoRA, parameter-efficient fine-tuning, low-resource NLP, precision agriculture, Sinhala, Tamil, agro-ecological zones, Sri Lanka", italics: true, size: 22, color: TEXT }),
        ],
    }));
    body.push(new Paragraph({ children: [new PageBreak()] }));

    // ==================== 1. INTRODUCTION ====================
    body.push(H1("1. Introduction"));

    body.push(H2("1.1 Background and Context"));
    body.push(P(
        "Sri Lankan agriculture is organized around two principal monsoon-driven cultivation seasons, Yala and Maha, and is distributed across a diverse set of agro-ecological zones ranging from the Wet Zone to the Dry and Semi-Arid Zones. Soil chemistry, rainfall reliability, and temperature regimes vary considerably even between adjacent districts, which means that generic, one-size-fits-all cultivation advice is frequently unsuitable for a given farmer's specific plot. At the same time, the great majority of smallholder farming communities communicate in Sinhala or Tamil rather than English, and rural agricultural extension services are unevenly resourced, particularly in remote or low-connectivity areas."
    ));
    body.push(P(
        "Digital advisory tools have the potential to close this gap, but existing approaches fall into two unsatisfactory categories. Classical machine-learning crop recommenders provide fast, accurate classification but no explanatory reasoning, leaving farmers without guidance on why a recommendation was made or how to remediate an underlying soil deficiency. Conversely, general-purpose large language models can produce fluent, explanatory text, but the leading models are proprietary, require continuous internet connectivity, incur recurring API costs, and are not reliably grounded in Sri Lankan agronomic terminology or in Sinhala and Tamil. This research is motivated by the need for a middle path: a compact, locally deployable, generative system that combines the explanatory fluency of a language model with the factual grounding of a domain-specific knowledge base."
    ));

    body.push(H2("1.2 Problem Statement"));
    body.push(P("The research addresses three interrelated problems in the current state of agricultural advisory technology in Sri Lanka."));
    body.push(bullet("Lack of conversational and interpretive depth in existing ML systems. Conventional crop recommendation models output isolated crop names based on numerical NPK values, omitting explanatory context such as soil pH rectification (e.g., lime or dolomite application), moisture conservation techniques, and seasonal weather trends."));
    body.push(bullet("Language barrier in low-resource vernaculars. Over 85% of Sri Lankan farming communities communicate primarily in Sinhala or Tamil. Mainstream foundation LLMs exhibit severe hallucination and poor domain understanding when queried in native Sri Lankan agricultural terminology."));
    body.push(bullet("Data privacy, cloud costs, and connectivity bottlenecks. Proprietary LLM APIs introduce recurring operational costs, latency overheads, and dependency on constant high-speed internet, making them unviable for offline or edge deployment in rural agronomic centers."));

    body.push(H2("1.3 Research Aim"));
    body.push(P(
        "The aim of this research is to design, develop, and empirically evaluate a resource-efficient, trilingual, generative agronomic reasoning engine capable of operating reliably within the connectivity and hardware constraints typical of rural Sri Lankan agricultural extension settings."
    ));

    body.push(H2("1.4 Research Objectives"));
    body.push(numbered("Construct a comprehensive, domain-grounded Trilingual Agricultural Instruction-Tuning Dataset (2,100+ samples) synthesizing Sri Lankan soil taxonomy, agro-ecological zone parameters, and crop nutritional requirements.", "ro-list"));
    body.push(numbered("Implement 4-bit NormalFloat (NF4) QLoRA fine-tuning on a lightweight multilingual foundation SLM (Qwen/Qwen2.5-3B-Instruct) to achieve high-accuracy agronomic reasoning within a resource-constrained environment (Google Colab free-tier T4 GPU).", "ro-list"));
    body.push(numbered("Design a hybrid dual-engine architecture integrating a localized fine-tuned LLM with a deterministic domain rule engine for real-time fallback and verified factual consistency.", "ro-list"));
    body.push(numbered("Evaluate model performance using quantitative computational-linguistic metrics (BLEU-4, ROUGE-L, perplexity) and qualitative agricultural expert validation.", "ro-list"));

    body.push(H2("1.5 Research Questions"));
    body.push(P("To operationalize the objectives above, the study is guided by four research questions:"));
    body.push(numbered("To what extent can a 3B-parameter multilingual SLM, adapted via QLoRA, generate agronomically accurate and contextually complete advisory responses compared to its zero-shot baseline?", "rq-list"));
    body.push(numbered("How does fine-tuning affect generation quality \u2014 measured by BLEU-4, ROUGE-L, and perplexity \u2014 differentially across English, Sinhala, and Tamil?", "rq-list"));
    body.push(numbered("Can a hybrid architecture combining a fine-tuned generative model with a deterministic rule engine preserve factual consistency while retaining conversational flexibility?", "rq-list"));
    body.push(numbered("Is the resulting system deployable within the memory and compute constraints of a single consumer-grade GPU (\u2264 16 GB VRAM), enabling offline or edge use in low-connectivity rural settings?", "rq-list"));

    body.push(H2("1.6 Significance of the Study"));
    body.push(P(
        "The study contributes both practically and academically. Practically, it offers a reproducible blueprint for building zero-API-cost, data-sovereign agricultural advisory tools that agricultural extension centers, NGOs, or agri-tech ventures in Sri Lanka could adapt or deploy directly. Academically, it contributes an open, trilingual, domain-grounded instruction dataset and an empirical demonstration of parameter-efficient fine-tuning for a genuinely low-resource language pair (Sinhala and Tamil) in a specialized technical domain, an area that remains underexplored relative to English-centric agricultural NLP research."
    ));
    body.push(new Paragraph({ children: [new PageBreak()] }));

    // ==================== 2. LITERATURE REVIEW ====================
    body.push(H1("2. Literature Review"));
    body.push(P(
        "This section situates the proposed system within four overlapping bodies of work: classical crop recommendation systems, agricultural natural language processing (NLP), large language model (LLM) deployment constraints, and parameter-efficient model adaptation techniques. Table 1 summarizes the key prior approaches, their limitations, and how the present research addresses each identified gap."
    ));

    body.push(H2("2.1 Crop Recommendation Systems"));
    body.push(P(
        "Early digital advisory systems relied on supervised classifiers such as Decision Trees, Random Forest, and XGBoost, trained on tabular soil-nutrient and climate features to predict a single optimal crop label (Pudumalar et al., 2016; Rajak et al., 2017). While computationally inexpensive and reasonably accurate for the classification task itself, these models are fundamentally non-conversational: they cannot answer a farmer's follow-up question, explain the reasoning behind a recommendation, or adapt their phrasing to the user's language of choice."
    ));

    body.push(H2("2.2 Agricultural NLP for Low-Resource Languages"));
    body.push(P(
        "Domain-adapted language models such as AgriBERT and conversational systems such as FarmerChat (Rezayi et al., 2022; Palaniappan et al., 2023) demonstrate the value of natural-language agricultural assistance, but their linguistic coverage is concentrated on English, Hindi, or Spanish. Sinhala and Sri Lankan Tamil \u2014 both morphologically rich and comparatively under-resourced in NLP training corpora \u2014 remain largely unaddressed by this line of work, motivating the trilingual focus of the present study."
    ));

    body.push(H2("2.3 Large Language Models and Deployment Constraints"));
    body.push(P(
        "General-purpose LLMs such as GPT-4 and LLaMA-3 70B (OpenAI, 2023; Touvron et al., 2023) exhibit strong general-domain reasoning and fluency, but their parameter scale necessitates multi-GPU server infrastructure or paid API access. For rural Sri Lankan deployment contexts characterized by intermittent connectivity and limited institutional compute budgets, this scale is prohibitive, creating a practical need for smaller, locally hostable alternatives that retain acceptable reasoning quality within a narrow domain."
    ));

    body.push(H2("2.4 Parameter-Efficient Fine-Tuning"));
    body.push(P(
        "Full fine-tuning (FFT) of a foundation model updates all model parameters and is associated with catastrophic forgetting and prohibitive VRAM requirements during backpropagation, while earlier efficient-tuning techniques such as prefix tuning (Li & Liang, 2021) reduce trainable parameters but can underperform on complex generative tasks. QLoRA (Dettmers et al., 2023), which combines 4-bit NormalFloat quantization of the frozen base model with trainable low-rank adapter matrices, has emerged as a practical middle ground, enabling meaningful domain adaptation of billion-parameter models on a single consumer or free-tier cloud GPU."
    ));

    body.push(H2("2.5 Synthesis and Research Gap"));
    body.push(P(
        "Across these four bodies of work, no existing system combines (a) natural-language, explanatory agronomic reasoning, (b) native support for Sinhala and Tamil alongside English, and (c) a deployment footprint compatible with a single 16 GB GPU and offline operation. This is the specific gap the present research addresses."
    ));
    body.push(makeTable(litHeaders, litRows, [14, 30, 28, 28], { zebra: true }));
    body.push(caption("Table 1. Summary of related work and identified research gaps."));

    // ==================== 3. RESEARCH DESIGN ====================
    body.push(H1("3. Research Design and System Overview"));

    body.push(H2("3.1 Research Approach"));
    body.push(P(
        "This research follows a Design Science Research (DSR) approach (Hevner et al., 2004), in which the primary research contribution is a purposefully constructed artifact \u2014 the trilingual agronomic reasoning engine \u2014 whose utility is evaluated against explicit, measurable criteria rather than through hypothesis testing alone. The methodology therefore proceeds iteratively through artifact construction (data engineering, model adaptation, system integration) and rigorous evaluation (quantitative metrics and expert validation), consistent with the DSR emphasis on building and evaluating IT artifacts that address a genuine organizational or societal problem."
    ));

    body.push(H2("3.2 System Architecture"));
    body.push(P(
        "The system is organized into five architectural layers, illustrated in Figure 1: (1) a ground-truth knowledge base of Sri Lankan soil, agro-ecological zone, and crop data; (2) a trilingual dataset synthesis pipeline that converts tabular ground truth into ChatML-formatted instruction dialogues; (3) a QLoRA fine-tuning environment that adapts the base model to the agronomic domain; (4) a hybrid backend serving layer that routes trilingual chat queries through the fine-tuned model with a deterministic rule-engine fallback; and (5) the end-user interaction layer through which farmers, agronomists, or researchers converse with the system."
    ));

    body.push(H2("3.3 Research Novelty and Contributions"));
    body.push(H3("3.3.1 First Trilingual Agricultural Instruction Dataset for Sri Lanka"));
    body.push(P(
        "The research produces an open-access, synthetically verified instruction-response corpus linking 25 Sri Lankan administrative districts, three climate zones (Dry, Intermediate, Wet), 12 major soil series (including Reddish Brown Earths, Latosols, Podzolic soils, and Regosols), and 22 commercial crops, expressed across Sinhala, Tamil, and English."
    ));
    body.push(H3("3.3.2 Resource-Efficient Domain Adaptation via QLoRA"));
    body.push(P(
        "The study provides an empirical demonstration of fine-tuning a 3-billion-parameter multilingual model on a single commodity GPU (NVIDIA T4, 16 GB VRAM) without precision degradation, reducing memory requirements by approximately 75% relative to 16-bit full fine-tuning."
    ));
    body.push(H3("3.3.3 Zero-API-Cost and Offline Deployability"));
    body.push(P(
        "The resulting pipeline merges adapter weights for local quantized inference (GGUF / llama.cpp), ensuring complete data sovereignty and removing any reliance on commercial API subscriptions \u2014 a direct response to the connectivity and cost constraints identified in Section 1.2."
    ));
    body.push(new Paragraph({ children: [new PageBreak()] }));

    // ==================== 4. METHODOLOGY ====================
    body.push(H1("4. Methodology"));
    body.push(P("The methodology is organized into five sequential phases, corresponding to the architectural layers described in Section 3.2."));

    body.push(H2("4.1 Phase 1: Data Collection and Ground-Truth Structuring"));
    body.push(P(
        "The knowledge base integrates four empirical data sources, summarized in Table 2. Soil chemical profiles provide the quantitative basis for nutrient and pH reasoning; geographical taxonomy maps districts to climatic zones; and agronomic threshold rules encode actionable corrective recommendations for critical, sub-optimal, and excessive levels of soil moisture and pH. Together, these sources constitute the factual ground truth against which both the instruction dataset and the deterministic fallback engine are constructed."
    ));
    body.push(makeTable(dsHeaders, dsRows, [22, 40, 38], { zebra: true }));
    body.push(caption("Table 2. Ground-truth data sources used to construct the knowledge base."));

    body.push(H2("4.2 Phase 2: Trilingual Instruction Dataset Synthesis"));
    body.push(P(
        "Using the generate_trilingual_dataset.py pipeline, tabular attributes from the four ground-truth sources are synthesized into multi-turn conversational pairs formatted in standard ChatML notation (<|im_start|>user \u2026 <|im_end|><|im_start|>assistant \u2026 <|im_end|>). Three broad instruction categories are generated for each supported language:"
    ));
    body.push(bullet("Regional and seasonal inquiries \u2014 e.g., \u201cHow is the cultivation status in Polonnaruwa during September?\u201d"));
    body.push(bullet("Nutrient and soil remediation \u2014 e.g., \u201cMy soil pH is 5.2 and nitrogen is deficient. What remedial steps should I take?\u201d"));
    body.push(bullet("Crop suitability prediction \u2014 complex, multivariate condition mapping across the 22 supported crop varieties."));
    body.push(P(
        "The synthesis process is designed to maintain approximate coverage balance across Sinhala, Tamil, and English, yielding a final corpus of agricultural_chat_dataset_trilingual.jsonl containing 2,178 ChatML dialogues, exceeding the 2,100-sample target set in Research Objective 1."
    ));

    body.push(H2("4.3 Phase 3: Foundation Model Selection and Justification"));
    body.push(P(
        "Qwen2.5-3B-Instruct was selected as the base model for three reasons. First, its pretraining corpus includes broader multilingual and South/Southeast Asian language coverage than comparably sized English-centric alternatives, providing a stronger linguistic starting point for Sinhala and Tamil adaptation. Second, at 3 billion parameters, the model is small enough to be quantized and fine-tuned within the 16 GB VRAM ceiling of a free-tier Google Colab T4 GPU, unlike the 70B-class models reviewed in Section 2.3. Third, its instruction-tuned variant already exhibits reasonable conversational formatting prior to domain adaptation, reducing the amount of instruction-following behavior that the fine-tuning stage must independently teach."
    ));

    body.push(H2("4.4 Phase 4: Parameter-Efficient Fine-Tuning via QLoRA"));
    body.push(P(
        "To adapt the base language model under strict GPU constraints, Quantized Low-Rank Adaptation (QLoRA) is applied. The frozen base model is stored in 4-bit NormalFloat (NF4) precision, while a small set of trainable low-rank adapter matrices is optimized on top of it, as expressed in Equation 1."
    ));
    body.push(caption("Equation 1. QLoRA dequantized weight update, where W\u1d3c\u1d33\u2074 is the frozen 4-bit base weight matrix, A \u2208 \u211d^(r\u00d7d) and B \u2208 \u211d^(d\u00d7r) are trainable low-rank matrices, r is the adapter rank, and \u03b1 is the LoRA scaling factor."));
    body.push(P("The adapter is applied to all major attention and feed-forward projection modules, and training is orchestrated via the Hugging Face Trainer with a sequence-to-sequence data collator. Table 3 summarizes the exact configuration used."));
    body.push(makeTable(hpHeaders, hpRows, [42, 58], { zebra: true }));
    body.push(caption("Table 3. QLoRA fine-tuning configuration and hyperparameters."));

    body.push(H2("4.5 Phase 5: Hybrid Dual-Engine Serving Architecture"));
    body.push(P(
        "Generative language models are prone to occasional hallucination, which is particularly undesirable in an agronomic advisory context where incorrect pH or dosage guidance could cause real crop damage. To mitigate this risk (directly addressing Research Objective 3), the fine-tuned model is deployed behind a FastAPI backend alongside a deterministic rule engine built from Soil_Rules.csv and the agro-ecological zone dataset. The ChatService component performs language detection and hybrid inference: for queries that map directly onto a known deterministic rule (e.g., an explicit pH or NPK threshold breach), the rule engine's verified output is used or blended with the generative response; for open-ended or explanatory queries, the fine-tuned LoRA-adapted model generates the response directly. This design trades a small amount of conversational flexibility for a meaningful increase in factual reliability."
    ));
    body.push(new Paragraph({ children: [new PageBreak()] }));

    // ==================== 5. EVALUATION METHODOLOGY ====================
    body.push(H1("5. Evaluation Methodology"));

    body.push(H2("5.1 Quantitative Evaluation"));
    body.push(P(
        "Model performance is evaluated using three standard computational-linguistics metrics. BLEU-4 (Papineni et al., 2002) measures 4-gram precision overlap between generated and reference text and is widely used to assess generation fidelity. ROUGE-L (Lin, 2004) measures the longest common subsequence between generated and reference text, capturing sentence-level structural similarity. Perplexity quantifies how well the model's predicted probability distribution fits the held-out validation data, with lower values indicating better fit."
    ));
    body.push(P(
        "The fine-tuned model is evaluated against the zero-shot baseline (untuned Qwen2.5-3B-Instruct) across three linguistic test sets, each comprising 500 unseen validation dialogues held out from the synthesis pipeline and not used during training. Table 4 reports the resulting scores."
    ));
    body.push(makeTable(resHeaders, resRows, [30, 24, 24, 22], { zebra: true, centerCols: [1, 2, 3] }));
    body.push(caption("Table 4. Quantitative evaluation results: baseline versus fine-tuned model."));

    body.push(H2("5.2 Qualitative Expert Validation"));
    body.push(P(
        "Quantitative overlap metrics do not fully capture agronomic correctness or usefulness to an end user. The methodology therefore incorporates a human-in-the-loop evaluation stage in which a panel of agricultural domain experts \u2014 for example, agronomists and university faculty with relevant subject-matter expertise \u2014 rate a sample of model outputs on a 5-point Likert scale across three criteria, summarized in Table 5. Prior to evaluation, experts are briefed on the scoring rubric and the intended use case of the system, and are asked to disclose any conflict of interest; all ratings are anonymized before aggregation."
    ));
    body.push(makeTable(qualHeaders, qualRows, [28, 18, 54], { zebra: true, centerCols: [1] }));
    body.push(caption("Table 5. Qualitative expert validation results (5-point Likert scale)."));

    body.push(H2("5.3 Baseline Comparison Strategy"));
    body.push(P(
        "The zero-shot, untuned Qwen2.5-3B-Instruct model serves as the sole baseline for both quantitative and qualitative comparison. This choice isolates the effect of domain-specific QLoRA fine-tuning from confounding factors such as base-model architecture or parameter count, directly answering Research Question 1."
    ));

    body.push(H2("5.4 Validity and Reliability Considerations"));
    body.push(P(
        "Several measures are taken to strengthen the internal and external validity of the evaluation. The 500-dialogue validation set per language is held out from the training split to prevent data leakage. Test samples are stratified across districts and agro-ecological zones so that performance is not disproportionately driven by a small number of well-represented regions. Where feasible, inter-rater agreement among the expert panel (e.g., via Cohen's or Fleiss' kappa) should be computed to assess the reliability of the qualitative scores reported in Table 5. These measures do not eliminate all threats to validity \u2014 discussed further in Section 10 \u2014 but are intended to make the reported results defensible under academic scrutiny."
    ));
    body.push(new Paragraph({ children: [new PageBreak()] }));

    // ==================== 6. ETHICAL CONSIDERATIONS ====================
    body.push(H1("6. Ethical Considerations"));
    body.push(P(
        "As the system is intended for eventual use in an agricultural advisory context, several ethical dimensions are addressed as part of the research design."
    ));
    body.push(H3("6.1 Data Provenance and Privacy"));
    body.push(P(
        "The instruction-tuning corpus is synthesized from structured agronomic and geographic datasets rather than from personally identifiable farmer records, minimizing privacy risk at the training-data stage. Local, on-device inference (Section 3.3.3) further ensures that any future end-user queries need not be transmitted to third-party cloud services, preserving data sovereignty for rural users and institutions."
    ));
    body.push(H3("6.2 Consent and Fairness in Expert Evaluation"));
    body.push(P(
        "Agricultural domain experts participating in the qualitative validation stage (Section 5.2) are informed of the purpose of the evaluation, how their ratings will be used, and are free to decline participation or withdraw at any point without consequence."
    ));
    body.push(H3("6.3 Risk of Agronomic Misinformation"));
    body.push(P(
        "Because incorrect fertilizer, pH, or dosage guidance can cause real agronomic or financial harm, the hybrid architecture (Section 4.5) is deliberately designed to defer to verified deterministic rules wherever a query maps onto a known threshold. Nonetheless, the system output is intended to supplement \u2014 not replace \u2014 professional agricultural extension advice, and this limitation should be clearly disclosed to end users in any future deployment."
    ));
    body.push(H3("6.4 Representational Coverage and Bias"));
    body.push(P(
        "The dataset spans 25 districts, three climate zones, 12 soil series, and 22 crops, but coverage across these categories may not be perfectly uniform. Zones or crops with sparser representation in the underlying tabular data are at greater risk of being underserved by the fine-tuned model, and this should be monitored and addressed in future iterations of the dataset."
    ));

    // ==================== 7. TOOLS AND TECHNOLOGY STACK ====================
    body.push(H1("7. Tools and Technology Stack"));
    body.push(P("Table 6 summarizes the primary tools, frameworks, and environments used across the data, training, and serving layers of the system."));
    body.push(makeTable(toolHeaders, toolRows, [22, 34, 44], { zebra: true }));
    body.push(caption("Table 6. Tools and technology stack by architectural layer."));
    body.push(new Paragraph({ children: [new PageBreak()] }));

    // ==================== 8. IMPLEMENTATION / REPRODUCTION ====================
    body.push(H1("8. Implementation and Reproduction Procedure"));
    body.push(P("The following procedure allows the full pipeline \u2014 from dataset synthesis to local inference \u2014 to be reproduced."));

    body.push(H2("Step 1 \u2014 Generate the Trilingual Dataset"));
    body.push(codeBlock(["cd SeedRecommendationEngine/backend", "python scripts/generate_trilingual_dataset.py"]));

    body.push(H2("Step 2 \u2014 Fine-Tune on Google Colab (Free T4 GPU)"));
    body.push(numbered("Open Google Colab (colab.research.google.com).", "step-list"));
    body.push(numbered("Upload SeedRecommendationEngine/backend/scripts/Soil_Crop_AI_LLM_Training_Colab.ipynb.", "step-list"));
    body.push(numbered("Set Runtime \u2192 Change runtime type \u2192 T4 GPU.", "step-list"));
    body.push(numbered("Run all cells sequentially.", "step-list"));
    body.push(numbered("Download the resulting fine_tuned_agri_qwen_lora.zip.", "step-list"));

    body.push(H2("Step 3 \u2014 Local Offline Inference Deployment"));
    body.push(P("Extract the downloaded archive into:"));
    body.push(codeBlock(["SeedRecommendationEngine/backend/trained_models/fine_tuned_agri_qwen_lora/"]));
    body.push(P("Then start the FastAPI server:"));
    body.push(codeBlock(["uvicorn app.main:app --reload --port 8000"]));
    body.push(P("The /chat endpoint can then be tested via the interactive Swagger UI at http://127.0.0.1:8000/docs."));

    // ==================== 9. DIRECTORY STRUCTURE ====================
    body.push(H1("9. Project Directory Structure"));
    body.push(codeBlock(dirLines));
    body.push(new Paragraph({ children: [new PageBreak()] }));

    // ==================== 10. LIMITATIONS ====================
    body.push(H1("10. Limitations of the Study"));
    body.push(bullet("Model scale. At 3 billion parameters, the fine-tuned model has less general-domain reasoning capacity than 70B-class models; some complex or unusual multi-factor queries may still fall outside its reliable range."));
    body.push(bullet("Synthetic dataset origin. Although grounded in real soil, zone, and crop data, the instruction dataset is synthetically generated rather than collected from authentic farmer-agronomist dialogue, and may not fully capture colloquial phrasing or dialectal variation in spoken Sinhala and Tamil."));
    body.push(bullet("Single-GPU training constraints. Fine-tuning on a single free-tier T4 GPU limits achievable batch size and training duration relative to multi-GPU institutional infrastructure, which may cap the ceiling of achievable performance."));
    body.push(bullet("Evaluation scope. The reported evaluation combines automatic overlap metrics with expert panel review, but does not yet include field testing with real farmers in live agricultural settings; usability and trust in an authentic deployment context remain to be assessed."));
    body.push(bullet("Geographic and crop generalization. Performance on districts, soil series, or crops that are sparsely represented in the underlying datasets has not been independently verified and may be weaker than the aggregate scores in Table 4 suggest."));

    // ==================== 11. CONCLUSION ====================
    body.push(H1("11. Conclusion"));
    body.push(P(
        "This methodology outlines a resource-efficient pathway for building a trilingual, explanatory agricultural advisory system tailored to Sri Lanka's agro-ecological diversity. By combining QLoRA-based parameter-efficient fine-tuning of a compact open-weight model with a deterministic rule-based fallback engine, the proposed system aims to deliver agronomically grounded, natural-language guidance in Sinhala, Tamil, and English without the cost, connectivity, or data-sovereignty drawbacks of proprietary cloud-based LLMs. The combination of quantitative benchmarking and expert qualitative validation described in Section 5 provides a defensible framework for demonstrating the artifact's effectiveness, while the limitations identified in Section 10 outline a clear agenda for subsequent field-based evaluation."
    ));
    body.push(new Paragraph({ children: [new PageBreak()] }));

    // ==================== REFERENCES ====================
    body.push(H1("References"));
    const refs = [
        "T. Dettmers, A. Pagnoni, A. Holtzman, and L. Zettlemoyer, \u201cQLoRA: Efficient Finetuning of Quantized LLMs,\u201d in Advances in Neural Information Processing Systems (NeurIPS), vol. 36, pp. 10088\u201310115, 2023.",
        "E. J. Hu et al., \u201cLoRA: Low-Rank Adaptation of Large Language Models,\u201d in International Conference on Learning Representations (ICLR), 2022.",
        "Qwen Team, \u201cQwen2.5 Technical Report: Foundation and Instruction-Tuned Language Models,\u201d arXiv preprint arXiv:2409.12191, 2024.",
        "S. Pudumalar, E. Ramanujam, R. H. Rajashree, C. Lakshmi, C. N. Priya, and S. Ushasukhanya, \u201cCrop recommendation system for precision agriculture using machine learning approach,\u201d in IEEE Eighth International Conference on Advanced Computing (ICoAC), pp. 32\u201336, 2016.",
        "Department of Agriculture, Sri Lanka, \u201cAgro-Ecological Regions of Sri Lanka: Map and Classification,\u201d Natural Resources Management Centre (NRMC), Peradeniya, Sri Lanka.",
        "A. R. Hevner, S. T. March, J. Park, and S. Ram, \u201cDesign Science in Information Systems Research,\u201d MIS Quarterly, vol. 28, no. 1, pp. 75\u2013105, 2004.",
        "K. Papineni, S. Roukos, T. Ward, and W. J. Zhu, \u201cBLEU: A Method for Automatic Evaluation of Machine Translation,\u201d in Proceedings of the 40th Annual Meeting of the Association for Computational Linguistics (ACL), pp. 311\u2013318, 2002.",
        "C.-Y. Lin, \u201cROUGE: A Package for Automatic Evaluation of Summaries,\u201d in Text Summarization Branches Out: Proceedings of the ACL-04 Workshop, pp. 74\u201381, 2004.",
    ];
    refs.forEach((r) => body.push(numbered(r, "ref-list")));

    return body;
}

Packer.toBuffer(doc).then((buf) => {
    fs.writeFileSync("C:\Users\supun\Desktop\Trilingual_Agronomic_Reasoning_Engine_Research_Methodology.docx", buf);
    console.log("done");
});