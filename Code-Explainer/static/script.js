// Function to toggle comments
function toggleComments() {
    const codeInput = document.getElementById('codeInput');
    const currentText = codeInput.value;
    const newText = addOrRemoveComments(currentText);
    codeInput.value = newText;
}

// Function to add or remove comments using OpenAI
function addOrRemoveComments(code) {
    const commentPrompt = `Add comments to the following code:\n\n${code}\n\nComments:`;
    const response = openai.Completion.create({
        engine: "text-davinci-003",
        prompt: commentPrompt,
        max_tokens: 100
    });
    const comments = response.choices[0].text.trim();
    
    // Toggle comments
    if (code.includes(comments)) {
        return code.replace(comments, '').trim();
    } else {
        return `${code}\n\n${comments}`.trim();
    }
}

// Function to explain code using OpenAI
function explainCode() {
    const codeInput = document.getElementById('codeInput').value;
    const language = guessLanguage(codeInput);
    
    openai.Completion.create({
        engine: "text-davinci-003",
        prompt: `Explain the following ${language} code in simple English:\n\n${codeInput}`,
        max_tokens: 150
    }).then((response) => {
        const explanation = response.choices[0].text.trim();
        displayExplanation(explanation);
    }).catch((error) => {
        console.error('Error explaining code:', error);
    });
}

// Function to translate code explanation
function translateCode() {
    const explanation = document.getElementById('result').textContent;
    const targetLanguage = document.getElementById('targetLanguage').value;
    
    const translations = translateExplanation(explanation, targetLanguage);
    displayTranslations(translations);
}

// Function to translate explanation to target language using Google Translate API
function translateExplanation(explanation, targetLanguage) {
    const translations = {};
    const parent = `projects/${project_id}/locations/global`;  // Replace with your actual Google Cloud project ID

    translate.TranslationServiceClient().translateText({
        parent: parent,
        contents: [explanation],
        targetLanguageCode: targetLanguage,
    }).then((responses) => {
        translations[targetLanguage] = responses[0].translations[0].translatedText;
    }).catch((error) => {
        console.error('Error translating explanation:', error);
    });

    return translations;
}

// Function to display explanation
function displayExplanation(explanation) {
    const resultElement = document.getElementById('result');
    resultElement.style.display = 'block';
    resultElement.textContent = explanation;
}

// Function to display translations
function displayTranslations(translations) {
    const resultElement = document.getElementById('result');
    resultElement.style.display = 'block';
    resultElement.textContent = `Translated to ${Object.keys(translations)[0]}: ${Object.values(translations)[0]}`;
}

// Function to detect programming language
function guessLanguage(code) {
    return guess.language_name(code);
}
