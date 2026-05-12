
document.addEventListener("DOMContentLoaded", function () {

    const formCadastro = document.getElementById("formCadastro");

    if (formCadastro) {

        formCadastro.addEventListener("submit", async (e) => {
            e.preventDefault();

            const dados = Object.fromEntries(
                new FormData(formCadastro)
            );

            try {
                
                // Envia os dados ao backend (rota /cadastrar) via POST
                const resp = await fetch('/api/cadastrar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(dados)
                });

                const result = await resp.json();

                document.getElementById('mensagem').innerText = result.message;
                formCadastro.reset();
            } 
            
            catch (err) {
                alert('Erro de comunicação com o servidor: ' + err);
            }

            console.log("Dados capturados:");
            console.log("Nome:", dados.nome);
            console.log("Email:", dados.email);
            console.log("Telefone:", dados.telefone);

            console.log(dados);
        });
    }



    // ============================================================================
    // 🔍 CONSULTA DE CLIENTES
    // ============================================================================

    // 💡 Essa parte funciona na página consulta.html
    const btnBuscar = document.getElementById('btnBuscar');

    if (btnBuscar) {
        btnBuscar.addEventListener('click', async () => {

            // Pega o nome digitado pelo usuário
            const nome = document.getElementById('campoBusca').value;

            // Faz uma requisição GET ao Flask, enviando o nome como parâmetro
            const resp = await fetch(`/api/buscar?nome=${nome}`);
            const clientes = await resp.json(); 

            const tabela = document.getElementById('tabelaResultados');
            tabela.innerHTML = ''; 

            // Para cada cliente retornado, cria uma nova linha na tabela HTML
            clientes.forEach(cli => {
                const row = `
                <tr>
                    <td>${cli.ID}</td>
                    <td>${cli.Nome}</td>
                    <td>${cli.CPF}</td>
                    <td>${cli.Email}</td>
                    <td>${cli.Telefone}</td>
                    <td>${cli.observacoes}</td>
                    <td><a href="/alterar?id=${cli.ID}" class="btn btn-sm btn-warning">Editar</a></td>
                </tr>`;
                tabela.innerHTML += row;
            });
        });
    }


    // ============================================================================
    // ✏️ ALTERAR CLIENTE
    // ============================================================================

    // 💡 Essa parte roda na página alterar.html
    const formAlterar = document.getElementById('formAlterar');

    if (formAlterar) {
        // 📎 Captura o ID do cliente a partir da URL (ex: /alterar?id=3)
        const urlParams = new URLSearchParams(window.location.search);
        const id = urlParams.get('id');

        const mensagem = document.getElementById('mensagem');

        fetch(`/api/cliente/${id}`)
            .then(r => r.json())
            .then(cli => {
                document.getElementById('clienteId').value = cli.ID;
                document.getElementById('nome').value = cli.Nome;
                document.getElementById('cpf').value = cli.CPF;
                document.getElementById('email').value = cli.Email;
                document.getElementById('telefone').value = cli.Telefone;
                document.getElementById('endereco').value = cli.Endereço;
                document.getElementById('observacoes').value = cli.Observações;
            });

        formAlterar.addEventListener('submit', async (e) => {
            e.preventDefault();

            const dados = {
                nome: nome.value,
                cpf: cpf.value,
                email: email.value,
                telefone: telefone.value,
                endereco: endereco.value,
                observacoes: observacoes.value
            };

            const resp = await fetch(`/api/atualizar/${id}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados)
            });

            const result = await resp.json();
            mensagem.innerText = result.message;
        });
    }
})