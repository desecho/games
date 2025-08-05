import { describe, expect, it, vi } from 'vitest'

import { useFormValidation } from '../formValidation'

describe('useFormValidation', () => {
  it('returns form ref and isValid function', () => {
    const { form, isValid } = useFormValidation()
    
    expect(form.value).toBe(null)
    expect(typeof isValid).toBe('function')
  })

  it('returns false when form is null', async () => {
    const { isValid } = useFormValidation()
    
    const result = await isValid()
    expect(result).toBe(false)
  })

  it('returns validation result when form exists', async () => {
    const { form, isValid } = useFormValidation()
    
    // Mock form with validate method
    const mockForm = {
      validate: vi.fn().mockResolvedValue({ valid: true })
    }
    
    form.value = mockForm as any
    
    const result = await isValid()
    expect(result).toBe(true)
    expect(mockForm.validate).toHaveBeenCalledOnce()
  })

  it('handles invalid form validation', async () => {
    const { form, isValid } = useFormValidation()
    
    // Mock form with validate method returning invalid
    const mockForm = {
      validate: vi.fn().mockResolvedValue({ valid: false })
    }
    
    form.value = mockForm as any
    
    const result = await isValid()
    expect(result).toBe(false)
    expect(mockForm.validate).toHaveBeenCalledOnce()
  })
})