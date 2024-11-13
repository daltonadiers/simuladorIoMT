document.getElementById('cep').addEventListener('blur', async function() {
  const cep = this.value.replace(/\D/g, '');
  if (cep.length === 8) {
    try {
      const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
      if (!response.ok) throw new Error("Erro ao buscar o CEP.");
      
      const data = await response.json();
      if (data.erro) throw new Error("CEP não encontrado.");
      
      document.getElementById('estado').value = data.uf;
      document.getElementById('cidade').value = data.localidade;
      document.getElementById('bairro').value = data.bairro;
      document.getElementById('rua').value = data.logradouro;
    } catch (error) {
      alert(error.message);
    }
  }
});

document.getElementById('userForm').addEventListener('submit', async function(event) {
  event.preventDefault();
  const user = {
    name: document.getElementById('name').value,
    birth: document.getElementById('birth').value,
    sex: document.getElementById('sex').value,
    cep: document.getElementById('cep').value,
    estado: document.getElementById('estado').value,
    cidade: document.getElementById('cidade').value,
    bairro: document.getElementById('bairro').value,
    rua: document.getElementById('rua').value,
    numero: document.getElementById('numero').value,
  };

  console.log(user);

  const response = await fetch('http://127.0.0.1:8000/api/cadastro', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  });
  const result = await response.json();
  console.log(result.message);
  alert(result.message || "Cadastro realizado com sucesso!");
});