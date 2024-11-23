import { useState } from "react";
import "../../App.css";
import "./UserRegister.css";
import { buscarEnderecoPorCep, cadastrarUsuario } from "../../components/api";

const UserRegister = () => {
  const [nome, setNome] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [nascimento, setNascimento] = useState("");
  const [sexo, setSexo] = useState("");
  const [cep, setCep] = useState("");
  const [estado, setEstado] = useState("");
  const [cidade, setCidade] = useState("");
  const [bairro, setBairro] = useState("");
  const [rua, setRua] = useState("");
  const [numero, setNumero] = useState("");
  const [tipos, setTipos] = useState([]);
  const [usuarios, setUsuarios] = useState([]);
  const [viewMode, setViewMode] = useState("add");
  const [editarEndereco, setEditarEndereco] = useState(false);

  const handleCepChange = async (e) => {
    const novoCep = e.target.value;
    setCep(novoCep);
    if (novoCep.length === 9) {
      try {
        const endereco = await buscarEnderecoPorCep(novoCep);
        if (endereco) {
          setEstado(endereco.estado);
          setCidade(endereco.cidade);
          setBairro(endereco.bairro);
          setRua(endereco.rua);
          setEditarEndereco(false);
        } else {
          setEstado("");
          setCidade("");
          setBairro("");
          setRua("");
          setEditarEndereco(true);
        }
      } catch (error) {
        alert(error.message);
        setEstado("");
        setCidade("");
        setBairro("");
        setRua("");
        setEditarEndereco(true);
      }
    }
  };

  const handleTipoChange = (e) => {
    const valorTipo = parseInt(e.target.value);
    if (e.target.checked) {
      setTipos([...tipos, valorTipo]);
    } else {
      setTipos(tipos.filter((tipo) => tipo !== valorTipo));
    }
  };

  const handleAddUser = async (event) => {
    event.preventDefault();

    if (nome && username && password && nascimento && sexo && cep && estado && cidade && bairro && rua && numero) {
      const novoUsuario = {
        name: nome,
        email: username,
        password: password,
        birth: new Date(nascimento).toISOString(),
        sex: sexo,
        postal_code: cep,
        state: estado,
        city: cidade,
        neighborhood: bairro,
        street: rua,
        house_number: numero,
        types: tipos,
      };

      try {
        const mensagem = await cadastrarUsuario(novoUsuario);
        alert(mensagem);

        setUsuarios([...usuarios, { ...novoUsuario, codigo: usuarios.length + 1 }]);
        setNome("");
        setUsername("");
        setPassword("");
        setNascimento("");
        setSexo("");
        setCep("");
        setEstado("");
        setCidade("");
        setBairro("");
        setRua("");
        setNumero("");
        setTipos([]);
      } catch (error) {
        alert(error.message);
      }
    } else {
      alert("Por favor, preencha todos os campos obrigatórios.");
    }
  };

  return (
    <div className="UserRegister">
      {viewMode === "add" ? (
        <form onSubmit={handleAddUser}>
          <h2>Cadastro de Usuário</h2>
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
            <label>E-mail:</label>
            <input
              type="email"
              placeholder="E-mail"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="input-field">
            <label>Senha:</label>
            <input
              type="password"
              placeholder="Senha"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
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
            </select>
          </div>
          <div className="input-field">
            <label>CEP:</label>
            <input
              type="text"
              placeholder="00000-000"
              value={cep}
              onChange={handleCepChange}
              required
            />
          </div>
          <div className="input-field">
            <label>Estado:</label>
            <input
              type="text"
              value={estado}
              onChange={(e) => setEstado(e.target.value)}
              readOnly={!editarEndereco}
            />
          </div>
          <div className="input-field">
            <label>Cidade:</label>
            <input
              type="text"
              value={cidade}
              onChange={(e) => setCidade(e.target.value)}
              readOnly={!editarEndereco}
            />
          </div>
          <div className="input-field">
            <label>Bairro:</label>
            <input
              type="text"
              value={bairro}
              onChange={(e) => setBairro(e.target.value)}
              readOnly={!editarEndereco}
            />
          </div>
          <div className="input-field">
            <label>Rua:</label>
            <input
              type="text"
              value={rua}
              onChange={(e) => setRua(e.target.value)}
              readOnly={!editarEndereco}
            />
          </div>
          <div className="input-field">
            <label>Número:</label>
            <input
              type="text"
              placeholder="Número"
              value={numero}
              onChange={(e) => setNumero(e.target.value)}
              required
            />
          </div>
          <button
            type="button"
            onClick={() => setEditarEndereco(!editarEndereco)}
            className="edit-button"
          >
            {editarEndereco ? "Bloquear edição" : "Editar endereço"}
          </button>
          <div className="input-field">
            <label>Tipos:</label>
            <div className="checkbox-group">
              <label>
                <input
                  type="checkbox"
                  value="1"
                  checked={tipos.includes(1)}
                  onChange={handleTipoChange}
                />
                Tipo 1
              </label>
              <label>
                <input
                  type="checkbox"
                  value="2"
                  checked={tipos.includes(2)}
                  onChange={handleTipoChange}
                />
                Tipo 2
              </label>
              <label>
                <input
                  type="checkbox"
                  value="3"
                  checked={tipos.includes(3)}
                  onChange={handleTipoChange}
                />
                Tipo 3
              </label>
            </div>
          </div>
          <button type="submit">Cadastrar</button>
        </form>
      ) : (
        <div className="data-table">
          <h2>Lista de Usuários</h2>
          {/* Tabela de usuários */}
        </div>
      )}
    </div>
  );
};

export default UserRegister;