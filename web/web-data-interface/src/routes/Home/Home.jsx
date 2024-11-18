import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getCollectedData } from "../../components/api";
import { useAuth } from "../../components/AuthContext";
import "./Home.css";

const dadosDeSaude = new Map([
  [1, "Pressão arterial"],
  [2, "SPO2"],
  [3, "Temperatura Corporal"]
]);

const Home = () => {
  const [measurements, setMeasurements] = useState([]);
  const [filteredMeasurements, setFilteredMeasurements] = useState([]);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [filterType, setFilterType] = useState("");
  const [inHouseFilter, setInHouseFilter] = useState("");
  const { token, clearToken } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMeasurements = async () => {
      if (token) {
        const data = await getCollectedData(token);
        if (data) {
          setMeasurements(data);
          setFilteredMeasurements(data);
        } else {
          console.error("Erro ao carregar os dados da API.");
        }
      }
    };

    fetchMeasurements();
  }, [token]);

  useEffect(() => {
    const filterMeasurements = () => {
      let filtered = measurements;

      if (startDate || endDate) {
        filtered = filtered.filter((measurement) => {
          const measurementDate = new Date(measurement.datetime);
          const start = startDate ? new Date(startDate) : null;
          const end = endDate ? new Date(endDate) : null;

          return (
            (!start || measurementDate >= start) &&
            (!end || measurementDate <= end)
          );
        });
      }

      if (filterType) {
        filtered = filtered.filter(
          (measurement) => measurement.type.toString() === filterType
        );
      }

      if (inHouseFilter !== "") {
        const inHouseValue = inHouseFilter === "true";
        filtered = filtered.filter(
          (measurement) => measurement.inhouse === inHouseValue
        );
      }

      setFilteredMeasurements(filtered);
    };

    filterMeasurements();
  }, [startDate, endDate, filterType, inHouseFilter, measurements]);

  const handleFilterChange = (event, setFilterFunction) => {
    setFilterFunction(event.target.value);
  };

  const handleLogout = () => {
    clearToken();
    navigate("/");
  };

  const formatDate = (date) => {
    const d = new Date(date);
    return d.toLocaleDateString("pt-BR") + " " + d.toLocaleTimeString("pt-BR");
  };

  return (
    <div className="Home">

      <div className="filter-section">
        <label htmlFor="start-date">Data Início </label>
        <input
          type="date"
          id="start-date"
          value={startDate}
          onChange={(e) => handleFilterChange(e, setStartDate)}
        />

        <label htmlFor="end-date" style={{ marginLeft: "10px" }}>Data Fim </label>
        <input
          type="date"
          id="end-date"
          value={endDate}
          onChange={(e) => handleFilterChange(e, setEndDate)}
        />

        <label htmlFor="filter-type" style={{ marginLeft: "10px" }}>Tipo de Medição </label>
        <select
          id="filter-type"
          className="select-filters"
          value={filterType}
          onChange={(e) => handleFilterChange(e, setFilterType)}
        >
          <option value="">Todos</option>
          <option value="1">Pressão arterial</option>
          <option value="2">SPO2</option>
          <option value="3">Temperatura Corporal</option>
        </select>

        <label htmlFor="inhouse-filter" style={{ marginLeft: "10px" }}>Em Casa </label>
        <select
          id="inhouse-filter"
          className="select-filters"
          value={inHouseFilter}
          onChange={(e) => handleFilterChange(e, setInHouseFilter)}
        >
          <option value="">Todos</option>
          <option value="true">Sim</option>
          <option value="false">Não</option>
        </select>
      </div>

      <div className="container">
        <h1>Medições</h1>
        {filteredMeasurements.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Tipo</th>
                <th>Valor 1</th>
                <th>Valor 2</th>
                <th>Em Casa</th>
                <th>Data/Hora</th>
              </tr>
            </thead>
            <tbody>
              {filteredMeasurements.map((measurement, index) => (
                <tr key={index}>
                  <td>{dadosDeSaude.get(measurement.type) || "Tipo desconhecido"}</td>
                  <td>{measurement.value1}</td>
                  <td>{measurement.value2}</td>
                  <td>{measurement.inhouse ? "Sim" : "Não"}</td>
                  <td>{formatDate(measurement.datetime)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>Nenhuma medição encontrada no período especificado.</p>
        )}
      </div>

      <div className="header">
        <button onClick={handleLogout} className="logout-button">
          Sair
        </button>
      </div>
    </div>
  );
};

export default Home;
