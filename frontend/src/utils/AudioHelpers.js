import axios from 'axios';

export const getResponse = async (transcription, addMessage) => {
    try {
      const result = await axios.post("http://localhost:8000/get_response", {
        text: transcription
      });

      const jsonObject = JSON.parse(result.data.response);
      const key = Object.keys(jsonObject)[0];
      const aiResponse = jsonObject[key];

      addMessage({ type: 'bot', text: aiResponse });  // Display the AI response in the UI

      return aiResponse;
    } catch (error) {
      console.error("Error getting response:", error);
      addMessage({ type: 'bot', text: "Error getting response." });
    }
};

export const getResponseAudio = async (text_response, addMessage) => {
    try {
        const result = await axios.post("http://localhost:8000/get_response_audio", {
            text: text_response
        }, {
            responseType: 'blob'
        });

        const audioBlob = new Blob([result.data], { type: 'audio/mpeg' });
        const audioUrl = URL.createObjectURL(audioBlob);

        const audio = new Audio(audioUrl);
        audio.play();
    } catch (error) {
        console.error("Error getting audio from model response:", error);
        addMessage({ type: 'bot', text: "Error getting audio response from model"});
    }
}

export const refresh = async (clearMessages, addMessage) => {
    try {
        await axios.delete("http://localhost:8000/clear_response");
        clearMessages();
        addMessage({ type: 'bot', text: "Conversation history has been cleared."});
    } catch (error) {
        console.error("Error clearing response:", error);
        addMessage({ type: 'bot', text: "Error clearing response." });
    }
}