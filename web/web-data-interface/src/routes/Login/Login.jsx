import { FaUser, FaLock } from "react-icons/fa";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

import "./Login.css";

const Login = () => {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = (event) => {
        event.preventDefault();

        if (username === "admin@admin" && password === "1234") {
            alert("Login bem-sucedido!");
            navigate("/home");
        } else {
            alert("Usuário ou senha incorretos!");
        }
    };

    return (
        <div className="Login">
            <div className="container">
                <form onSubmit={handleSubmit}>
                    <h1>Acesso ao sistema</h1>
                    <div className="input-field">
                        <input type="email" placeholder='E-mail' required 
                            onChange={(e) => setUsername(e.target.value)}/>
                        <FaUser className="icon"/>
                    </div>
                    <div className="input-field">
                        <input type="password" placeholder='Senha' required 
                            onChange={(e) => setPassword(e.target.value)}/>
                        <FaLock className="icon"/>
                    </div>

                    <div className="recall-forget">
                        <label>
                            <input type="checkbox"/>
                            Lembrar login
                        </label>
                        <a href="#">Esqueceu a senha?</a>
                    </div>

                    <div>
                        <button>Entrar</button>
                    </div>

                    <div className="signup-link">
                        <p>
                            Deseja criar uma nova conta? <a href="#">Clique aqui!</a>
                        </p>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default Login
