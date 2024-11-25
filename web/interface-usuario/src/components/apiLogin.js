export async function getToken(username, password) {
    const url = "https://iomt-data-api-7752107602.us-central1.run.app/token";
    const data = new URLSearchParams({ username, password });
  
    try {
      const response = await fetch(url, {
        method: "POST",
        body: data,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });
  
      if (response.ok) {
        const jsonResponse = await response.json();
        return jsonResponse.access_token;
      } else {
        console.error(
          `Erro ao obter token: ${response.status}, ${await response.text()}`
        );
        return null;
      }
    } catch (error) {
      console.error(`Erro de rede ou outra falha: ${error}`);
      return null;
    }
  }
  
  export async function getCollectedData(token) {
    const url =
      "https://iomt-data-api-7752107602.us-central1.run.app/collected-data/";
  
    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
  
      if (response.ok) {
        return await response.json();
      } else {
        console.error(
          `Erro ao acessar dados: ${response.status}, ${await response.text()}`
        );
        return null;
      }
    } catch (error) {
      console.error(`Erro de rede ou outra falha: ${error}`);
      return null;
    }
  }
  
  export async function deleteData(token, seq) {
    const url = `https://iomt-data-api-7752107602.us-central1.run.app/collected-data/${seq}`;
  
    try {
      const response = await fetch(url, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });
  
      if (response.ok) {
        const result = await response.json();
        console.log("Item deletado com sucesso:", result);
        return result;
      } else {
        console.error(
          "Erro ao deletar o item:",
          response.status,
          response.statusText
        );
        throw new Error(`Erro ao deletar o item. CÃ³digo: ${response.status}`);
      }
    } catch (error) {
      console.error("Erro durante a chamada DELETE:", error);
      throw error;
    }
  }
  
  export async function postData(token, data) {
    const url = `https://iomt-data-api-7752107602.us-central1.run.app/collected-data/`;
  
    try {
      const jsonData = JSON.stringify(data);
      const response = await fetch(url, {
        method: "POST",
        body: jsonData,
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });
  
      const result = await response.json();
  
      if (response.ok) {
        return { success: true, data: result };
      } else {
        return { success: false, error: result };
      }
    } catch (error) {
      console.error("Erro ao enviar dados:", error);
      throw error;
    }
  }
  
  export async function putData(token, seq, data) {
    const url = `https://iomt-data-api-7752107602.us-central1.run.app/collected-data/${seq}`;
  
    const response = await fetch(url, {
      method: "PUT",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
  
    const result = await response.json();
  
    if (response.ok) {
      return { success: true, data: result };
    } else {
      return { success: false, error: result };
    }
  }
  
  export async function getUserName(token) {
    const url = "https://iomt-user-api-7752107602.us-central1.run.app/users/";
  
    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
  
      if (response.ok) {
        return await response.json();
      } else {
        console.error(
          `Erro ao acessar dados: ${response.status}, ${await response.text()}`
        );
        return null;
      }
    } catch (error) {
      console.error(`Erro de rede ou outra falha: ${error}`);
      return null;
    }
  }
  
  export async function inHouse(user) {
    if (!("geolocation" in navigator)) {
      throw new Error("Geolocation is not supported by your browser");
    }
  
    return new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const currentLat = position.coords.latitude;
          const currentLng = position.coords.longitude;
  
          const userLat = user.latitude;
          const userLng = user.longitude;
  
          const calculateDistance = (lat1, lng1, lat2, lng2) => {
            const toRad = (value) => (value * Math.PI) / 180;
            const R = 6371000; // Raio da Terra em metros
  
            const dLat = toRad(lat2 - lat1);
            const dLng = toRad(lng2 - lng1);
  
            const a =
              Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(toRad(lat1)) *
                Math.cos(toRad(lat2)) *
                Math.sin(dLng / 2) *
                Math.sin(dLng / 2);
  
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
            return R * c;
          };
  
          const distance = calculateDistance(
            userLat,
            userLng,
            currentLat,
            currentLng
          );
  
          resolve(distance <= 300);
        },
        (error) => {
          reject(error);
        }
      );
    });
  }