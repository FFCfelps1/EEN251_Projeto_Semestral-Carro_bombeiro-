# Documentação LaTeX - Carro Bombeiro Teleoprado

Este diretório contém os arquivos fonte para a geração da documentação técnica do projeto seguindo as normas da ABNT.

## Estrutura de Arquivos

- `main.tex`: Arquivo principal que contém a estrutura do documento e o conteúdo das seções.
- `referencias.bib`: Arquivo de bibliografia no formato BibTeX.

## Requisitos para Compilação

Para compilar estes arquivos e gerar o PDF, você precisará de uma distribuição LaTeX instalada (como MiKTeX ou TeX Live) e da classe `abntex2`.

### Comandos de Compilação

1. `pdflatex main.tex`
2. `bibtex main`
3. `pdflatex main.tex`
4. `pdflatex main.tex`

Ou utilize um editor como TeXstudio, VSCode (com extensão LaTeX Workshop) ou o serviço online Overleaf.

## Notas

Os nomes dos integrantes e da instituição estão como placeholders `[Nome ...]` no arquivo `main.tex`. Lembre-se de editá-los antes da versão final.
