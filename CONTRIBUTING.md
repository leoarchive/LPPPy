# Contribuindo com LPPPy

Obrigado por querer contribuir com o projeto!

# Contribuindo
## Reporte um bug
Os bugs são reportados na [página de issues do projeto](https://github.com/leozamboni/LPPPy/issues). Antes de abrir uma nova issue, certifique-se de que ela já não foi reportada anteriormente. Assim que seu problema for reportado ele será analisado por um contribuidor ou mantenedor do projeto. Se houver dúvidas sobre seu problema, responda o mais rápido possível.

Reportar bugs e problemas é bem vindo e muito importante para o projeto!

## Perguntas
Se precisar fazer alguma pergunta sobre o projeto ou sobre qualquer coisa, você também pode enviar através da [página de issues](https://github.com/leozamboni/LPPPy/issues), através do [discord](https://discord.gg/FpmXy28Y) ou caso o projeto exploda entre em contato pelo servidor IRC irc.leonardo.moe em #main.

## Requisitar mudanças

- Crie um fork do projeto;
- Implemente suas alterações seguindo as [convenções de código](#Convenções-de-código);
- Faça squash dos commits para que fiquem em apenas um commit (isso pode ser feito com ```git rebase -i```);
- Se esforce para que tenha uma mensagem de commit decente;
- Abra um pull request e resolva qualquer comentário/dúvida que possa ser feita por um contribuidor ou mantenedor do projeto.
	
## Buildando

Utilizando nix package:
```
nix-shell -p nix/shell.nix;
make clean;
build;
```

build é um script que utiliza cython e gcc para gerar o binário estático. 

## Convenções de código

- Todo arquivo deve ser licenciado e conter o header com instruções da licença GPL 3 (pode ser copiado de um arquivo já existente);
- Todo o código deve ser escrito em inglês, salva exceções para nomes referente a palavras reservadas da sintaxe do LPP (```programa```, ```início```, ```fim```, …).
- Todo arquivo deve ser formatado utilizando black

## Licença de contribuições

Este projeto está aberto para contribuições, sugestões e comentários. Todas as contribuições, sugestões e comentários enviados são aceitos sob a licença GPL 3. Você declara que, se não possuir direitos autorais no código, tem autoridade para enviá-lo sob a licença GPL 3. Todos os comentários, sugestões ou contribuições não são confidenciais.
