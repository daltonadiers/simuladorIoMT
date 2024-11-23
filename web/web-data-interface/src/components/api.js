export async function getToken(username, password) {
    const url = "https://iomt-data-api-7752107602.us-central1.run.app/token";
    const data = new URLSearchParams({ username, password });
    
    try {
        const response = await fetch(url, {
            method: "POST",
            body: data,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        });

        if (response.ok) {
            const jsonResponse = await response.json();
            return jsonResponse.access_token;
        } else {
            console.error(`Erro ao obter token: ${response.status}, ${await response.text()}`);
            return null;
        }
    } catch (error) {
        console.error(`Erro de rede ou outra falha: ${error}`);
        return null;
    }
}

export async function getCollectedData(token) {
    const url = "https://iomt-data-api-7752107602.us-central1.run.app/collected-data/";

    try {
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        });

        if (response.ok) {
            return await response.json();
        } else {
            console.error(`Erro ao acessar dados: ${response.status}, ${await response.text()}`);
            return null;
        }
    } catch (error) {
        console.error(`Erro de rede ou outra falha: ${error}`);
        return null;
    }
}