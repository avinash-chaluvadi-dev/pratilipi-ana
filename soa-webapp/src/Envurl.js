export const Envurl = () => {
  let domainUrl = window.location.href;
  let url = new URL(domainUrl);
  return `${url.origin}/vmt-soa-gateway/v1`;
};
