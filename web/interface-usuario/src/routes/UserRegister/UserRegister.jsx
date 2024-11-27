import { useState } from "react";
import { Form, Button, Container, Row, Col, InputGroup, FormCheck } from "react-bootstrap";
import { buscarEnderecoPorCep, cadastrarUsuario } from "../../components/apiCadastro";
import './UserRegister.css'

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
    <Container className="py-5">
      <Row className="justify-content-center">
        <Col md={8} lg={6}>
        <div className="register-card">
          <h2 className="text-center mb-4">Cadastro de Usuário</h2>
          <p className="text-center mb-4">Já tem uma conta? <Button href="/login" className="login">Login</Button></p>
          <Form onSubmit={handleAddUser}>
            <Form.Group controlId="formNome" className="mb-3">
              <Form.Label>Nome</Form.Label>
              <Form.Control
                type="text"
                maxLength="50"
                placeholder="Nome"
                value={nome}
                onChange={(e) => setNome(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group controlId="formEmail" className="mb-3">
              <Form.Label>E-mail</Form.Label>
              <Form.Control
                type="email"
                placeholder="E-mail"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group controlId="formSenha" className="mb-3">
              <Form.Label>Senha</Form.Label>
              <Form.Control
                type="password"
                placeholder="Senha"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group controlId="formNascimento" className="mb-3">
              <Form.Label>Data de Nascimento</Form.Label>
              <Form.Control
                type="date"
                value={nascimento}
                onChange={(e) => setNascimento(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group controlId="formSexo" className="mb-3">
              <Form.Label>Sexo</Form.Label>
              <Form.Select value={sexo} onChange={(e) => setSexo(e.target.value)} required>
                <option value="">Selecione</option>
                <option value="M">Masculino</option>
                <option value="F">Feminino</option>
              </Form.Select>
            </Form.Group>

            <Form.Group controlId="formCep" className="mb-3">
              <Form.Label>CEP</Form.Label>
              <Form.Control
                type="text"
                placeholder="00000-000"
                value={cep}
                onChange={handleCepChange}
                required
              />
            </Form.Group>

            <Row>
              <Col md={6}>
                <Form.Group controlId="formEstado" className="mb-3">
                  <Form.Label>Estado</Form.Label>
                  <Form.Control
                    type="text"
                    value={estado}
                    onChange={(e) => setEstado(e.target.value)}
                    readOnly={!editarEndereco}
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group controlId="formCidade" className="mb-3">
                  <Form.Label>Cidade</Form.Label>
                  <Form.Control
                    type="text"
                    value={cidade}
                    onChange={(e) => setCidade(e.target.value)}
                    readOnly={!editarEndereco}
                  />
                </Form.Group>
              </Col>
            </Row>

            <Form.Group controlId="formBairro" className="mb-3">
              <Form.Label>Bairro</Form.Label>
              <Form.Control
                type="text"
                value={bairro}
                onChange={(e) => setBairro(e.target.value)}
                readOnly={!editarEndereco}
              />
            </Form.Group>

            <Form.Group controlId="formRua" className="mb-3">
              <Form.Label>Rua</Form.Label>
              <Form.Control
                type="text"
                value={rua}
                onChange={(e) => setRua(e.target.value)}
                readOnly={!editarEndereco}
              />
            </Form.Group>

            <Form.Group controlId="formNumero" className="mb-3">
              <Form.Label>Número</Form.Label>
              <Form.Control
                type="text"
                placeholder="Número"
                value={numero}
                onChange={(e) => setNumero(e.target.value)}
                required
              />
            </Form.Group>

            <Button
              variant="outline-secondary"
              onClick={() => setEditarEndereco(!editarEndereco)}
              className="mb-3 w-100"
            >
              {editarEndereco ? "Bloquear edição" : "Editar endereço"}
            </Button>

            <Form.Group className="mb-3">
              <Form.Label>Tipos</Form.Label>
              <div>
                {[1, 2, 3].map((tipo) => (
                  <FormCheck
                    key={tipo}
                    type="checkbox"
                    label={`Tipo ${tipo}`}
                    value={tipo}
                    checked={tipos.includes(tipo)}
                    onChange={handleTipoChange}
                  />
                ))}
              </div>
            </Form.Group>

            <Button variant="primary" type="submit" className="w-100">
              Cadastrar
            </Button>
          </Form>
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default UserRegister;
