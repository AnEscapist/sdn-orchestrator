
function parseMemoryIntGBFromBytes(memoryStr) {
  //memoryStr: memory in bytes, ex. '12355'
  //return: memory in gigabytes, as an int
  let bytes_in_gigabyte = Math.pow(1024, 3);
  return parseInt((parseInt(memoryStr)/bytes_in_gigabyte));
}

function getZeroToNArray(n) {
  if (n===0) return [0];
  else return Array.from(Array(n+1).keys());
}

function getOneToNArray(n) {
  if (n===0) return [];
  else return getZeroToNArray(n-1).map(x => x+1)
}

export {parseMemoryIntGBFromBytes, getZeroToNArray, getOneToNArray}


