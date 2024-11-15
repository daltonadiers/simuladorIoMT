import { useState } from "react";
import "./Home.css";

const Home = () => {
  const [nome, setNome] = useState("");
  const [nascimento, setNascimento] = useState("");
  const [sexo, setSexo] = useState("");
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");
  const [usuarios, setUsuarios] = useState([]);
  const [viewMode, setViewMode] = useState("add");

  const handleAddUser = (event) => {
    event.preventDefault();

    if (nome && nascimento && sexo && latitude && longitude) {
      const novoCodigo = usuarios.length > 0 ? usuarios[usuarios.length - 1].codigo + 1 : 1;
      const novoUsuario = {
        codigo: novoCodigo,
        nome,
        nascimento: new Date(nascimento).toLocaleDateString(),
        sexo,
        latitude: parseFloat(latitude),
        longitude: parseFloat(longitude),
      };
      setUsuarios([...usuarios, novoUsuario]);
      setNome("");
      setNascimento("");
      setSexo("");
      setLatitude("");
      setLongitude("");
      alert("Usuário cadastrado com sucesso!");
    } else {
      alert("Por favor, preencha todos os campos obrigatórios.");
    }
  };

  return (
    <div className="Home">
      <nav className="menu">
        <button onClick={() => setViewMode("add")}>Adicionar Usuário</button>
        <button onClick={() => setViewMode("view")}>Ver Usuários</button>
      </nav>

      {viewMode === "add" ? (
        <form onSubmit={handleAddUser}>
          <h1>Cadastro de Usuário</h1>
          <div className="input-field">
            <label>Nome:</label>
            <input
              type="text"
              maxLength="50"
              placeholder="Nome"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              required
            />
          </div>
          <div className="input-field">
            <label>Data de Nascimento:</label>
            <input
              type="date"
              value={nascimento}
              onChange={(e) => setNascimento(e.target.value)}
              required
            />
          </div>
          <div className="input-field">
            <label>Sexo:</label>
            <select
              value={sexo}
              onChange={(e) => setSexo(e.target.value)}
              required
            >
              <option value="">Selecione</option>
              <option value="M">Masculino</option>
              <option value="F">Feminino</option>
              <option value="O">Outro</option>
            </select>
          </div>
          <div className="input-field">
            <label>Latitude:</label>
            <input
              type="number"
              step="0.0001"
              placeholder="Latitude"
              value={latitude}
              onChange={(e) => setLatitude(e.target.value)}
              required
            />
          </div>
          <div className="input-field">
            <label>Longitude:</label>
            <input
              type="number"
              step="0.0001"
              placeholder="Longitude"
              value={longitude}
              onChange={(e) => setLongitude(e.target.value)}
              required
            />
          </div>
          <button type="submit">Cadastrar Usuário</button>
        </form>
      ) : (
        <div className="data-table">
          <h1>Lista de Usuários</h1>
          {usuarios.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>Código</th>
                  <th>Nome</th>
                  <th>Nascimento</th>
                  <th>Sexo</th>
                  <th>Latitude</th>
                  <th>Longitude</th>
                </tr>
              </thead>
              <tbody>
                {usuarios.map((usuario) => (
                  <tr key={usuario.codigo}>
                    <td>{usuario.codigo}</td>
                    <td>{usuario.nome}</td>
                    <td>{usuario.nascimento}</td>
                    <td>{usuario.sexo}</td>
                    <td>{usuario.latitude}</td>
                    <td>{usuario.longitude}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>Nenhum usuário cadastrado.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default Home;
