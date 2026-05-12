try {
    document.addEventListener("DOMContentLoaded", function () {
        const formCadastro = document.getElementById("formCadastro");

        if (formCadastro) {
            formCadastro.addEventListener("submit", async (e) => {
                e.preventDefault();

                const dados = Object.fromEntries(
                    new FormData(formCadastro)
                );

                try {
                    const resp = await fetch("/cadastrar", {
                        method: "POST",
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(dados)
                    });

                    const result = await resp.json();

                    document.getElementById('mensagem').innerText = result.message;

                    formCadastro.reset();
                } 
                
                catch (err) {
                    alert("Erro de comunicação com o servidor!" + err);
                }

                console.log("Dados Capturados: ");
                console.log("Nome: " + dados.nome);
                console.log("CPF: " + dados.cpf);
                console.log("Email: " + dados.email);
                console.log("Telefone: " + dados.telefone);
                console.log("Endereço: " + dados.endereco);
                console.log("Observação: " + dados.observacao);
            });
        }
    })
} 

catch (e) {
    console.error("Erro ao carregar a página!: " + e);
    document.write("<h1>Erro ao carregar a página!</h1><p>" + e + "</p>");
}

// Consulta 

const btnBuscar = document.getElementById("btnBuscar");

if (btnBuscar !== null) {
    console.log("ihfewihiew")
    btnBuscar.addEventListener("click", async () => {
        const nome = document.getElementById("campoBusca").value;

        const resp = await fetch(`/buscar?nome=${nome}`);
        const clientes = await resp.json();

        const tabela = document.getElementById("tabelaResultados");
        tabela.innerHTML = "";

        clientes.forEach(cli => {
            const row = `
                <tr>
                    <td>${cli.ID}</td>
                    <td>${cli.Nome}</td>
                    <td>${cli.CPF}</td>
                    <td>${cli["E-mail"]}</td> 
                    <td>${cli.Telefone}</td>
                    <td><a href="/alterar?id=${cli.ID}" class="btn">Editar</a></td>
                </tr>
            `;

            tabela.innerHTML += row;
        });
    });
}

const formAlterar = document.getElementById("formAlterar");

if(formAlterar !== null){

    formAlterar.addEventListener("submit", async (e) => {
        e.preventDefault();

        const dados = {
            nome: nome.value,
            cpf: cpf.value,
            email: email.value,
            telefone: telefone.value,
            endereco: endereco.value,
            observacao: observacao.value
        };

        const resp = await fetch(`/api/atualizar/${id}`, {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        const result = await resp.json();
        mensagem.innerText = result.message;

    });

}