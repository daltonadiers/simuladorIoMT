import { FaUser, FaLock } from "react-icons/fa";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getToken } from "../../components/api";
import { useAuth } from "../../components/AuthContext";
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
        <div className="Login">
            <div className="container">
                <form onSubmit={handleSubmit}>
                    <h1>Acesso ao sistema</h1>
                    <div className="input-field">
                        <input 
                            type="email" 
                            placeholder="E-mail" 
                            required 
                            onChange={(e) => setUsername(e.target.value)} 
                        />
                        <FaUser className="icon" />
                    </div>
                    <div className="input-field">
                        <input 
                            type="password" 
                            placeholder="Senha" 
                            required 
                            onChange={(e) => setPassword(e.target.value)} 
                        />
                        <FaLock className="icon" />
                    </div>

                    <div className="recall-forget">
                        <label>
                            <input type="checkbox" /> Lembrar login
                        </label>
                        <a href="#">Esqueceu a senha?</a>
                    </div>

                    <div>
                        <button type="submit">Entrar</button>
                    </div>

                    <div className="signup-link">
                        <p>
                            Deseja criar uma nova conta? <a href="#">Clique aqui!</a>
                        </p>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Login;