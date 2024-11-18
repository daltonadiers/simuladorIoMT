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
  const [usuarios, setUsuarios] = useState([]);
  const [viewMode, setViewMode] = useState("add");

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
        } else {
          setEstado("");
          setCidade("");
          setBairro("");
          setRua("");
        }
      } catch (error) {
        alert(error.message);
        setEstado("");
        setCidade("");
        setBairro("");
        setRua("");
      }
    }
  };

  const handleAddUser = async (event) => {
    event.preventDefault();

    if (nome && username && password && nascimento && sexo && cep && estado && cidade && bairro && rua && numero) {
      const novoUsuario = {
        nome,
        username,
        password,
        nascimento: new Date(nascimento).toISOString().split('T')[0],
        sexo,
        cep,
        estado,
        cidade,
        bairro,
        rua,
        numero,
      };

      try {
        const mensagem = await cadastrarUsuario(novoUsuario);
        alert(mensagem);

        // Atualiza a lista de usuários (opcional)
        setUsuarios([...usuarios, { ...novoUsuario, codigo: usuarios.length + 1 }]);

        // Reseta os campos
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
              <option value="O">Outro</option>
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
            <input type="text" value={estado} readOnly />
          </div>
          <div className="input-field">
            <label>Cidade:</label>
            <input type="text" value={cidade} readOnly />
          </div>
          <div className="input-field">
            <label>Bairro:</label>
            <input type="text" value={bairro} readOnly />
          </div>
          <div className="input-field">
            <label>Rua:</label>
            <input type="text" value={rua} readOnly />
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
          <button type="submit">Cadastrar</button>
        </form>
      ) : (
        <div className="data-table">
          <h2>Lista de Usuários</h2>
          {usuarios.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>Código</th>
                  <th>Nome</th>
                  <th>E-mail</th>
                  <th>Nascimento</th>
                  <th>Sexo</th>
                  <th>CEP</th>
                  <th>Estado</th>
                  <th>Cidade</th>
                  <th>Bairro</th>
                  <th>Rua</th>
                  <th>Número</th>
                </tr>
              </thead>
              <tbody>
                {usuarios.map((usuario) => (
                  <tr key={usuario.codigo}>
                    <td>{usuario.codigo}</td>
                    <td>{usuario.nome}</td>
                    <td>{usuario.username}</td>
                    <td>{usuario.nascimento}</td>
                    <td>{usuario.sexo}</td>
                    <td>{usuario.cep}</td>
                    <td>{usuario.estado}</td>
                    <td>{usuario.cidade}</td>
                    <td>{usuario.bairro}</td>
                    <td>{usuario.rua}</td>
                    <td>{usuario.numero}</td>
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

export default UserRegister;
