export const buscarEnderecoPorCep = async (cep) => {
  const cepLimpo = cep.replace(/\D/g, '');
  if (cepLimpo.length === 8) {
    try {
      const response = await fetch(`https://viacep.com.br/ws/${cepLimpo}/json/`);
      if (!response.ok) throw new Error("Erro ao buscar o CEP.");

      const data = await response.json();
      if (data.erro) throw new Error("CEP não encontrado.");

      return {
        estado: data.uf,
        cidade: data.localidade,
        bairro: data.bairro,
        rua: data.logradouro,
      };
    } catch (error) {
      throw new Error(error.message);
    }
  }
  return null;
};

export const cadastrarUsuario = async (usuario) => {
  console.log(usuario)
  try {
    const response = await fetch('https://iomt-user-api-7752107602.us-central1.run.app/users/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(usuario),
    });

    const result = await response.json();

    if (!response.ok) {
      return result.message || "Erro ao cadastrar o usuário: Verifique seu endereço";
    }

    return result.message || "Cadastro realizado com sucesso!";
  } catch (error) {
    throw new Error("Erro ao cadastrar o usuário.");
  }
};
