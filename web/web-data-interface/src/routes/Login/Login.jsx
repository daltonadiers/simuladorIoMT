import { FaUser, FaLock } from "react-icons/fa";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getToken } from "../../components/api";
import { useAuth } from "../../components/AuthContext";
import { Container, Form, Button, Row, Col } from "react-bootstrap";
import "./Login.css";

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const { saveToken } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const token = await getToken(username, password);

            if (token) {
                saveToken(token);
                navigate("/home");
            } else {
                alert("Usuário ou senha incorretos!");
            }
        } catch (error) {
            console.error("Erro durante o login:", error);
            alert("Ocorreu um erro. Tente novamente mais tarde.");
        }
    };

    return (
        <Container className="login-container">
            <Row className="justify-content-center">
                <Col md={6} lg={4}>
                    <div className="login-card">
                        <h2 className="text-center">Acesso ao Sistema</h2>
                        <Form onSubmit={handleSubmit}>
                            <Form.Group controlId="formBasicEmail" className="mb-3">
                                <Form.Label>E-mail</Form.Label>
                                <div className="input-group">
                                    <Form.Control 
                                        type="email" 
                                        placeholder="E-mail" 
                                        required 
                                        onChange={(e) => setUsername(e.target.value)} 
                                    />
                                    <div className="input-group-append">
                                        <span className="input-group-text">
                                            <FaUser />
                                        </span>
                                    </div>
                                </div>
                            </Form.Group>

                            <Form.Group controlId="formBasicPassword" className="mb-3">
                                <Form.Label>Senha</Form.Label>
                                <div className="input-group">
                                    <Form.Control 
                                        type="password" 
                                        placeholder="Senha" 
                                        required 
                                        onChange={(e) => setPassword(e.target.value)} 
                                    />
                                    <div className="input-group-append">
                                        <span className="input-group-text">
                                            <FaLock />
                                        </span>
                                    </div>
                                </div>
                            </Form.Group>

                            <Button variant="primary" type="submit" block>
                                Entrar
                            </Button>
                        </Form>

                        <div className="signup-link text-center mt-3">
                            <p>
                                Deseja criar uma nova conta? <a href="https://iomtwebcadastro.sytes.net">Clique aqui!</a>
                            </p>
                        </div>
                    </div>
                </Col>
            </Row>
        </Container>
    );
};

export default Login;