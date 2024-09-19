FROM ghcr.io/huggingface/text-generation-inference:latest
ENV MODEL_ID=distilbert/distilgpt2
# preapre the image to be used by non-root user
RUN mkdir -p /data && chmod 777 /data && useradd --create-home --uid 100000 job
USER 100000
